#!/usr/bin/env node
/**
 * LinkedIn Contact Info Scraper
 * Reads lead-generator-first-third-preview.csv, visits each profile,
 * clicks "Contact info", and extracts email/website/phone.
 * Writes enriched output to leads/leads-with-contact.csv
 */
import { execSync } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { parse } from 'csv-parse/sync';
import { stringify } from 'csv-stringify/sync';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = '/home/claw/.openclaw/workspace';
const INPUT = `${WORKSPACE}/leads/lead-generator-first-third-preview.csv`;
const OUTPUT = `${WORKSPACE}/leads/leads-with-contact.csv`;
const SESSION = 'datanova-leads';

function ab(cmd, timeout = 30000) {
  try {
    const result = execSync(
      `agent-browser --session-name ${SESSION} ${cmd}`,
      { timeout, encoding: 'utf8', cwd: WORKSPACE }
    );
    return result.trim();
  } catch (e) {
    return e.stdout?.trim() || '';
  }
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function extractContactInfo(snapshot) {
  const email = snapshot.match(/[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/)?.[0] || '';
  const websiteMatch = snapshot.match(/\/url:\s*(https?:\/\/(?!linkedin\.com)[^\s\n]+)/);
  const website = websiteMatch ? websiteMatch[1] : '';
  const phoneMatch = snapshot.match(/\b(\+?[\d\s\-().]{7,20})\b/g);
  const phone = phoneMatch ? phoneMatch[0].trim() : '';
  return { email, website, phone };
}

async function scrapeContactInfo(profileUrl) {
  console.log(`  → Opening profile: ${profileUrl}`);
  ab(`open '${profileUrl}'`);
  ab('wait --load networkidle', 35000);

  // Find and click Contact info link
  const snap1 = ab('snapshot -i');
  const contactRef = snap1.match(/link "Contact info" \[ref=(e\d+)\]/)?.[1];
  if (!contactRef) {
    console.log('  ⚠ No Contact info link found');
    return { email: '', website: '', phone: '' };
  }

  ab(`click @${contactRef}`);
  ab('wait 2000', 5000);

  // Get full snapshot including dialog
  const snap2 = ab('snapshot');

  // Check for contact overlay URL approach too
  const overlayUrl = profileUrl.replace(/\/?$/, '/overlay/contact-info/');
  let contactSnap = snap2;

  // If dialog didn't open properly, navigate directly to overlay
  if (!snap2.includes('dialog "Contact info"')) {
    console.log('  → Trying direct overlay URL');
    ab(`open '${overlayUrl}'`);
    ab('wait --load networkidle', 35000);
    contactSnap = ab('snapshot');
  }

  const info = extractContactInfo(contactSnap);
  console.log(`  ✓ email=${info.email || '(none)'} website=${info.website || '(none)'}`);
  return info;
}

async function main() {
  const csv = readFileSync(INPUT, 'utf8');
  const records = parse(csv, { columns: true, skip_empty_lines: true });

  console.log(`Processing ${records.length} leads...\n`);
  const results = [];

  for (let i = 0; i < records.length; i++) {
    const lead = records[i];
    console.log(`[${i + 1}/${records.length}] ${lead.first_name} ${lead.last_name} @ ${lead.company_name}`);

    let info = { email: '', website: '', phone: '' };
    try {
      info = await scrapeContactInfo(lead.linkedin_url);
    } catch (e) {
      console.log(`  ✗ Error: ${e.message}`);
    }

    results.push({
      ...lead,
      email: info.email,
      website: info.website,
      phone: info.phone,
    });

    // Polite delay between profiles (2-4s)
    const delay = 2000 + Math.random() * 2000;
    await sleep(delay);
  }

  // Write output
  const output = stringify(results, { header: true });
  writeFileSync(OUTPUT, output);
  console.log(`\n✓ Done. Output written to ${OUTPUT}`);

  const withEmail = results.filter(r => r.email).length;
  const withWebsite = results.filter(r => r.website).length;
  console.log(`  ${withEmail}/${results.length} have email`);
  console.log(`  ${withWebsite}/${results.length} have website`);
}

main().catch(console.error);

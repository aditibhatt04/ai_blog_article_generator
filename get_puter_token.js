#!/usr/bin/env node

/**
 * Helper script to get Puter auth token
 * This will open your browser and prompt you to log in to Puter
 * The token will be saved to your .env file
 */

const fs = require('fs');
const path = require('path');
const { getAuthToken } = require('@heyputer/puter.js/src/init.cjs');

async function main() {
    try {
        console.log('🔐 Puter Auth Token Retriever');
        console.log('==============================\n');
        console.log('This will open your browser to log in to Puter and get your auth token.\n');

        console.log('Requesting auth token from Puter...');
        const authToken = await getAuthToken();

        if (!authToken) {
            console.error('❌ Failed to get auth token');
            process.exit(1);
        }

        console.log('\n✅ Auth token received!');
        console.log(`Token: ${authToken.substring(0, 20)}...${authToken.substring(authToken.length - 10)}\n`);

        // Write to .env file
        const envPath = path.join(__dirname, '.env');
        let envContent = '';

        if (fs.existsSync(envPath)) {
            envContent = fs.readFileSync(envPath, 'utf-8');
            // Remove existing PUTER_AUTH_TOKEN line if it exists
            envContent = envContent
                .split('\n')
                .filter(line => !line.startsWith('PUTER_AUTH_TOKEN='))
                .join('\n');
        }

        // Add the new token
        if (envContent && !envContent.endsWith('\n')) {
            envContent += '\n';
        }
        envContent += `PUTER_AUTH_TOKEN=${authToken}`;

        fs.writeFileSync(envPath, envContent);

        console.log('✅ Token saved to .env file!\n');
        console.log('Next steps:');
        console.log('1. Restart your Django server');
        console.log('2. Try generating a blog from a YouTube video\n');
        console.log('The blog generator will now use Puter.js AI! 🚀');

    } catch (error) {
        console.error('❌ Error:', error.message);
        console.error('\nIf browser auth didn\'t work, you can manually get the token:');
        console.error('1. Go to https://puter.com');
        console.error('2. Log in to your account');
        console.error('3. Open browser DevTools (F12)');
        console.error('4. Go to Application → Local Storage');
        console.error('5. Find your puter.com domain and look for "auth_token"');
        console.error('6. Copy the value and add to your .env file:');
        console.error('   PUTER_AUTH_TOKEN=<paste-token-here>');
        process.exit(1);
    }
}

main();

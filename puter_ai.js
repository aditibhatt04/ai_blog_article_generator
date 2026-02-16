#!/usr/bin/env node

const { init } = require('@heyputer/puter.js/src/init.cjs');

/**
 * Script to call Puter.js AI from Node.js
 * Usage: node puter_ai.js "your prompt here"
 * Returns JSON with {success: true, content: "..."} or {success: false, error: "..."}
 */

async function main() {
    try {
        // Get auth token from environment variable
        const authToken = process.env.PUTER_AUTH_TOKEN;
        if (!authToken) {
            outputJSON({ success: false, error: 'PUTER_AUTH_TOKEN environment variable not set' });
            process.exit(1);
        }

        // Get prompt from command line argument
        let prompt = process.argv[2];

        if (!prompt) {
            outputJSON({ success: false, error: 'No prompt provided' });
            process.exit(1);
        }

        const response = await generateContent(prompt, authToken);
        outputJSON({ success: true, content: response });
        process.exit(0);

    } catch (error) {
        outputJSON({ success: false, error: error.message });
        process.exit(1);
    }
}

async function generateContent(prompt, authToken) {
    try {
        // Initialize Puter.js with auth token
        const puter = init(authToken);

        console.error('[DEBUG] Initializing Puter.js with auth token...');
        console.error('[DEBUG] Calling puter.ai.chat()...');

        // Call Puter.js AI
        const response = await puter.ai.chat(prompt, {
            model: 'gpt-5-nano' // Using GPT-5 nano model
        });

        console.error('[DEBUG] Response received');
        console.error('[DEBUG] Response type:', typeof response);
        console.error('[DEBUG] Response length:', response ? response.length : 0);

        if (!response) {
            throw new Error('Puter.js returned empty response');
        }

        return response;
    } catch (error) {
        console.error('[ERROR] Puter.js error:', error.message);
        throw error;
    }
}

function outputJSON(obj) {
    // Use Buffer to ensure proper encoding
    const json = JSON.stringify(obj);
    process.stdout.write(json);
}

main();

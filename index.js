import 'dotenv/config';
import chalk from 'chalk';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;

const username = process.argv[2];

if (!username) {
    console.error("Please provide a GitHub username: github-activity <username>");
    process.exit(1);
}

async function fetchActivity(user) {
    try {
        const response = await fetch(`https://api.github.com/users/${user}/events`, {
            headers: {
                ...(GITHUB_TOKEN && { Authorization: `Bearer ${GITHUB_TOKEN}` }),
                'User-Agent': 'node-js-cli'
        }
    });
        
        if (response.status === 404) {
        console.error("User not found.");
        return;
        }
        
        if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status}`);
        }

        const events = await response.json();

        if (events.length === 0) {
        console.log(`${user} has no recent public activity.`);
        return;
        }

        events.slice(0, 10).forEach(event => {
        let action;
        const repo = event.repo.name;

        switch (event.type) {
            case "PushEvent":
            const commitCount = event.payload.commits?.length || 0;
            action = `${chalk.green('Pushed')} ${chalk.bold(commitCount)} commit(s) to ${repo}`;
            break;
            case "IssuesEvent":
            action = `${event.payload.action.charAt(0).toUpperCase() + event.payload.action.slice(1)} an issue in ${repo}`;
            break;
            case "WatchEvent":
            action = `Starred ${repo}`;
            break;
            case "CreateEvent":
            action = `${chalk.magenta('Created')} ${event.payload.ref_type} in ${repo}`;
            break;
            default:
            action = `${event.type.replace("Event", "")} in ${repo}`;
        }
        console.log(`- ${action}`);
        });

    } catch (error) {
        console.error("Error details:", error.cause || error.message);
    }
}

fetchActivity(username);


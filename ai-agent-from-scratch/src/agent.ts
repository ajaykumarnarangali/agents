import { GoogleGenAI } from "@google/genai";
import "dotenv/config";
import readline from "node:readline/promises";
import { stdin, stdout } from "node:process";
import {
    getCurrentTimeInTimeZone,
    check_appointment_availability,
    schedule_appointment,
    delete_appointment
} from "./helper.js";


const apiKey = process.env.GEMINI_API_KEY;

if (!apiKey) {
    throw new Error("GEMINI_API_KEY is not configured");
}

const gemini = new GoogleGenAI({ apiKey });

const messages = [] as any;

const SYSTEM_PROMPT = `
You are an appointment scheduler AI agent. You're always interacting with a system. You have the ability to do function calls.
Your response can be either a reply to the user, or to the system to do a function call. But you cannot reply to the user and system in the same turn.
So your response should be in JSON format as specified - 

{
  "to": "",
  "message": "",
  "function_call": {
    "function": "",
    "arguments": []
  }
}

I will explain the keys -

1. to - values could be system or user, depending on whom you are replying
2. message - plain text message. Use this only if you are replying to the user not system
3. function_call - Use this only if you are replying to the system. It is a JSON object that determines which function to call, and it's arguments.
4 a. function - name of the function
4 b. arguments - An array of arguments for the function call where each array item is the value for the argument.

Available functions:
💡
function name - check_appointment_availability
arguments - datetime (ISO 8601 format, UTC timezone)

function name - schedule_appointment
arguments - datetime (ISO 8601 format, UTC timezone), name (String), email (string)

function name - delete_appointment
arguments - datetime (ISO 8601 format, UTC timezone), name (String), email (string)

Here are some instructions –
💡
Chat with user who wants to schedule an appointment with your owner.
Ask if they have any choice for the appointment time.
You must be able to understand that users might be from a different time zone.
Always use their timezone while chatting about times and dates to the user.
Before scheduling the appointment, you must ask their name and email.
Your owner is in IST timezone (+05:30)
Time and date now for your owner is ${getCurrentTimeInTimeZone("Asia/Kolkata")}
`

const functionMap = {
    'check_appointment_availability': check_appointment_availability,
    'schedule_appointment': schedule_appointment,
    'delete_appointment': delete_appointment
}
type FunctionName = keyof typeof functionMap;

async function llmInteraction(content: string) {
    if (!content.trim()) {
        console.log("Agent:", "type something idiot");
        return;
    };

    messages.push({
        role: "user",
        parts: [{ text: content.trim() }],
    });

    const response = await gemini.models.generateContent({
        model: "gemini-3.1-flash-lite",
        contents: messages,
        config: {
            systemInstruction: SYSTEM_PROMPT,
            maxOutputTokens: 256
        },
    });

    const assistantResponse = response.text ?? "";

    messages.push({
        role: "model",
        parts: [{ text: assistantResponse }],
    });

    return response.text;
}

interface AgentResponse {
    to: "system" | "user";
    message: string;
    function_call?: {
        function: string;
        arguments: any[];
    };
}
async function process_llm_response(response: any) {

    const parsedResponse: AgentResponse = JSON.parse(response);
    if (parsedResponse.to === "user") {
        console.log("Agent:", parsedResponse.message);
        return;
    }

    const functionName = parsedResponse.function_call?.function;
    const args = parsedResponse.function_call?.arguments ?? [];

    if (functionName && functionName in functionMap) {
        // Type assertion: Treat the selected function as accepting a variable number of string arguments.
        const selectedFunction = functionMap[functionName as FunctionName] as (
            ...args: string[]
        ) => string;

        const function_response = selectedFunction(...args);
        const llm_response = await llmInteraction(function_response);
        await process_llm_response(llm_response);
    }

}


async function main() {
    const rl = readline.createInterface({
        input: stdin,
        output: stdout,
    });

    try {
        while (true) {
            const content = await rl.question("You: ");

            if (content.trim().toLowerCase() === "exit") {
                break;
            }

            if (!content.trim()) continue;
            const response = await llmInteraction(content);
            process_llm_response(response);
        }
    } finally {
        rl.close();
    }
}

main();

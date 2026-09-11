import cors from "cors";
import express from "express";
import OpenAI from "openai";

const SYSTEM_PROMPT = `You are a customer-support executive for our
Food ordering app named Tomato.

Your job is to identify the customer's main
problem and urgency. Answer them related to there query.

Use professional language. If user has an issue,
use words like I understand your frustration,
I am really sorry for your trouble etc.

Do not answer any other question which is not
related to Ordering Food query, refund query,
order tracking status query or company policy query.
`;

const app = express();
const client = new OpenAI();
const model = process.env.OPENAI_MODEL ?? "gpt-4o-mini";
const history = [];

// Serialize history operations so simultaneous requests cannot interleave turns.
let historyQueue = Promise.resolve();
function useHistory(operation) {
  const result = historyQueue.then(operation);
  historyQueue = result.catch(() => {});
  return result;
}

app.use(cors());
app.use(express.text({ type: "*/*" }));

app.post("/api/chat", async (req, res, next) => {
  if (typeof req.body !== "string") {
    res.status(400).type("text/plain").send("Request body must be text");
    return;
  }

  try {
    const answer = await useHistory(async () => {
      history.push({ role: "user", content: req.body });

      const apiResponse = await client.responses.create({
        model,
        instructions: SYSTEM_PROMPT,
        input: history,
        store: false,
      });

      history.push({ role: "assistant", content: apiResponse.output_text });
      return apiResponse.output_text;
    });

    res.type("text/plain").send(answer);
  } catch (error) {
    next(error);
  }
});

app.delete("/api", async (_req, res, next) => {
  try {
    await useHistory(async () => {
      history.length = 0;
    });
    res.status(200).send();
  } catch (error) {
    next(error);
  }
});

app.use((error, _req, res, _next) => {
  console.error(error);
  res.status(500).type("text/plain").send("Unable to process the chat request");
});

export default app;

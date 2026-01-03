function $(id) {
  return document.getElementById(id);
}

const btn = $("generateBtn");
const input = $("productName");
const errorEl = $("error");
const questionsEl = $("questions");
const answerEl = $("answer");

function setError(msg) {
  if (!errorEl) return;
  errorEl.textContent = msg || "";
  errorEl.style.display = msg ? "block" : "none";
}

function setLoading(isLoading) {
  if (!btn) return;
  btn.disabled = isLoading;
  btn.textContent = isLoading ? "Generating..." : "Generate";
}

function setQuestionsList(items) {
  if (!questionsEl) return;
  questionsEl.innerHTML = "";
  (items || []).forEach((q) => {
    const li = document.createElement("li");
    li.textContent = q;
    questionsEl.appendChild(li);
  });
}

function setAnswer(text) {
  if (!answerEl) return;
  answerEl.textContent = text || "";
}

async function ensurePuterSession() {
  if (typeof puter === "undefined") {
    throw new Error("Puter SDK not loaded. Check the script tag.");
  }

  try {
    if (puter?.auth?.getUser) {
      const user = await puter.auth.getUser();
      if (user) return;
    }
  } catch (_) {
    // ignore and sign in below
  }

  if (puter?.auth?.signIn) {
    await puter.auth.signIn();
    return;
  }

  throw new Error("Puter auth not available.");
}

function parseJsonFromText(text) {
  const match = String(text).match(/\{[\s\S]*\}/);
  const jsonText = match ? match[0] : text;
  return JSON.parse(jsonText);
}

async function generateQuestionsPuter(productName) {
  const prompt = `
You are an ecommerce content agent.
Generate 5 high-quality customer FAQ questions for the product: "${productName}".
Output as JSON only: {"questions":[ "...", "..." ]}
`.trim();

  const resp = await puter.ai.chat(prompt, { model: "gpt-4o-mini" });
  const text = typeof resp === "string" ? resp : (resp?.text ?? String(resp));
  const json = parseJsonFromText(text);

  const questions = Array.isArray(json.questions) ? json.questions : [];
  return questions.map((x) => String(x)).filter(Boolean).slice(0, 5);
}

async function generateAnswerPuter(productName) {
  const prompt = `
You are a skincare FAQ assistant.
Write a helpful, safe, non-medical answer to: "What is ${productName} and how do I use it safely?"
Use bullet points or numbered lists. Mention patch test + sunscreen guidance. Avoid medical claims.
`.trim();

  const resp = await puter.ai.chat(prompt, { model: "gpt-4o-mini" });
  return typeof resp === "string" ? resp : (resp?.text ?? String(resp));
}

// Optional fallback backend (LangGraph mock/HF)
async function generateViaBackend(productName) {
  const r = await fetch("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ productName }),
  });

  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data?.error || "Backend failed");
  return {
    questions: Array.isArray(data.questions) ? data.questions : [],
    answer: data.answer || "",
  };
}

async function onGenerate() {
  setError("");
  setQuestionsList([]);
  setAnswer("");
  setLoading(true);

  const productName = (input?.value || "").trim();
  if (!productName) {
    setLoading(false);
    setError("Please enter a product name.");
    return;
  }

  try {
    // Primary path: Puter client-side (real LLM, no keys)
    await ensurePuterSession();
    const [questions, answer] = await Promise.all([
      generateQuestionsPuter(productName),
      generateAnswerPuter(productName),
    ]);

    setQuestionsList(questions);
    setAnswer(answer);
  } catch (e) {
    console.error(e);

    // Fallback path: backend (LangGraph mock/HF)
    try {
      const out = await generateViaBackend(productName);
      setQuestionsList(out.questions);
      setAnswer(out.answer);
      setError("Puter failed; used backend fallback.");
    } catch (e2) {
      console.error(e2);
      setError((e2 && e2.message) ? e2.message : "Generation failed.");
    }
  } finally {
    setLoading(false);
  }
}

if (btn) btn.addEventListener("click", onGenerate);

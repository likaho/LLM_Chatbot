"use client";
import Image from "next/image";
import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function Home() {
  const [done, setDone] = useState(false);
  const [agent, setAgent] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [question, setQuestion] = useState("");

  const handleSend = async (e) => {
    e.preventDefault();
    if (!question) return;

    setLoading(true);
    let result;
    result = await fetch(`/api/sqlagent/?q=${question}`);
    const json = await result.json();
    
    setResult(json);
    setDone(true);
    setLoading(false);
  };

  return (
    <div className="flex h-screen">
      <div className="flex-grow h-screen flex flex-col justify-between mx-auto max-w-4xl px-4 chat-area">
        {" "}
        <div className="chat-space">
          {result && !loading && <Markdown content={result.results} />}
          {result && result.query && !loading && (
            <Markdown content={result.query} />
          )}
        </div>
        <form
          onSubmit={handleSend}
          className="flex items-center py-3 input-box"
        >
          <input
            type="text"
            className="flex-1 p-2 border rounded-l-md input"
            placeholder="Ask Question"
            value={question}
            onInput={(e) => {
              setQuestion(e.target.value);
            }}
          />
          <button
            type="submit"
            className="bg-orange-600 text-dark p-2 rounded-r-md hover:bg-orange-400"
          >
            send
          </button>
        </form>
        {loading && "Loading..."}
      </div>
    </div>
  );
}

const Markdown = ({ content }) => (
  <ReactMarkdown
    className="prose mt-1 w-full break-words prose-p:leading-relaxed  py-3 px-3 mark-down"
    remarkPlugins={[remarkGfm]}
    components={{
      a: ({ node, ...props }) => (
        <a {...props} style={{ color: "#27afcf", fontWeight: "bold" }} />
      ),
    }}
  >
    {content}
  </ReactMarkdown>
);

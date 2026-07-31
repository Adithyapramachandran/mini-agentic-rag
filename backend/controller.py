import time

from backend.retriever import retrieve
from backend.reasoner import decide
from backend.actor import lookup_product
from backend.logger import save_trace


def run_agent(query):

    trace = []

    docs = retrieve(query)

    trace.append({
        "step": "retrieval",
        "documents_found": len(docs),
        "docs": docs
    })

    decision = decide(
        query,
        docs
    )

    trace.append({
        "step": "reasoning",
        "decision": decision,
        "reason":
            "Price/Stock query -> TOOL"
            if "TOOL" in decision
            else "Knowledge Base contains answer"
    })

    # TOOL PATH
    if "TOOL" in decision:

        product = None

        if "pro" in query.lower():
            product = "Pro Plan"

        elif "basic" in query.lower():
            product = "Basic Plan"

        elif "enterprise" in query.lower():
            product = "Enterprise Plan"

        elif "addon" in query.lower():
            product = "AI Addon"

        start_time = time.time()

        tool_result = lookup_product(
            product
        )

        latency = round(
            time.time() - start_time,
            4
        )

        trace.append({
            "step": "tool",
            "tool_name": "CSV Lookup",
            "latency_seconds": latency,
            "result": tool_result
        })

        answer = (
            f"{product} costs "
            f"${tool_result['price']} "
            f"and stock is "
            f"{tool_result['stock']}"
        )

    # KB PATH
    else:

        if len(docs) > 0:

            context = "\n".join(docs)

            answer_prompt = f"""
User Question:
{query}

Context:
{context}

Answer the question using only the provided context.

If the answer is not available in the context, reply:

Information not available in the knowledge base.
"""

            from backend.reasoner import model

            response = model.generate_content(
                answer_prompt
            )

            answer = response.text

        else:

            answer = (
                "Information not available "
                "in the knowledge base."
            )

    trace.append({
        "step": "answer",
        "answer": answer
    })

    save_trace(trace)

    return answer, trace
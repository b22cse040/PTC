# tool_search.py

import json
import sqlite3
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class ToolSearchResult:
    tools: List[Dict[str, Any]]
    tools_callable: Dict[str, Callable]


class ToolSearchModule:
    def __init__(
        self,
        db_path: str,
        model_name: str = "answerdotai/ModernBERT-base",
    ):
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row

        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

        self._create_tables()

    def _create_tables(self) -> None:
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS tools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                input_schema TEXT NOT NULL,
                input_example TEXT NOT NULL
            )
            """
        )

        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS tool_embeddings (
                tool_id INTEGER PRIMARY KEY,
                embedding BLOB NOT NULL,
                FOREIGN KEY (tool_id)
                    REFERENCES tools(id)
                    ON DELETE CASCADE
            )
            """
        )

        self.db.commit()

    def add_tool(self, tool: Dict[str, Any]) -> None:
        """
        Add a tool to the database.

        The embedding is generated only from:

            [CLS] tool[name] [SEP] tool[description]
        """

        name = tool["name"]
        description = tool["description"]

        embedding_text = (
            f"[CLS] tool[{name}] [SEP] tool[{description}]"
        )

        embedding = self.model.encode(
            embedding_text,
            normalize_embeddings=True,
        )

        self.db.execute(
            """
            INSERT OR REPLACE INTO tools (
                name,
                description,
                input_schema,
                input_example
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                description,
                json.dumps(tool["input-schema"]),
                json.dumps(tool["input_example"]),
            ),
        )

        row = self.db.execute(
            """
            SELECT id
            FROM tools
            WHERE name = ?
            """,
            (name,),
        ).fetchone()

        tool_id = row["id"]

        self.db.execute(
            """
            INSERT OR REPLACE INTO tool_embeddings (
                tool_id,
                embedding
            )
            VALUES (?, ?)
            """,
            (
                tool_id,
                embedding.astype(np.float32).tobytes(),
            ),
        )

        self.db.commit()

    def search_tools(
        self,
        query: str,
        k: int,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the top-k tools relevant to the query.

        Semantic search is performed using only the tool
        name and description embeddings.
        """

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        ).astype(np.float32)

        rows = self.db.execute(
            """
            SELECT
                t.id,
                t.name,
                t.description,
                t.input_schema,
                t.input_example,
                e.embedding
            FROM tools t
            JOIN tool_embeddings e
                ON t.id = e.tool_id
            """
        ).fetchall()

        results = []

        for row in rows:
            embedding = np.frombuffer(
                row["embedding"],
                dtype=np.float32,
            )

            # Both embeddings are normalized,
            # so dot product is cosine similarity.
            score = float(
                np.dot(query_embedding, embedding)
            )

            results.append(
                {
                    "tool_id": row["id"],
                    "name": row["name"],
                    "description": row["description"],
                    "input_schema": json.loads(
                        row["input_schema"]
                    ),
                    "input_example": json.loads(
                        row["input_example"]
                    ),
                    "score": score,
                }
            )

        results.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return results[:k]

    def get_callable_dict(
        self,
        TOOLS: Dict[str, Callable],
        result_search_tools: List[Dict[str, Any]],
    ) -> Dict[str, Callable]:
        """
        Build the callable dictionary for the retrieved tools.

        Maps tool names from the search results to their
        corresponding Python implementations.
        """

        tools_callable = {}

        for tool in result_search_tools:
            tool_name = tool["name"]

            if tool_name not in TOOLS:
                raise KeyError(
                    f"Tool '{tool_name}' exists in the database "
                    f"but is missing from TOOLS."
                )

            tools_callable[tool_name] = TOOLS[tool_name]

        return tools_callable

    def invoke(
        self,
        query: str,
        k: int,
        TOOLS: Dict[str, Callable],
    ) -> ToolSearchResult:
        """
        Search for relevant tools and resolve their
        corresponding Python callables.
        """

        tools = self.search_tools(
            query=query,
            k=k,
        )

        tools_callable = self.get_callable_dict(
            TOOLS=TOOLS,
            result_search_tools=tools,
        )

        return ToolSearchResult(
            tools=tools,
            tools_callable=tools_callable,
        )

    def close(self) -> None:
        """Close the database connection."""

        self.db.close()

if __name__ == "__main__":
    from src.tools.tool_implementation import TOOLS
    from src.tools.tool_ingestion import TOOLS_DEFINTION

    tool_search = ToolSearchModule(
        db_path="tools.db",
    )

    for tool in TOOLS_DEFINTION:
        tool_search.add_tool(tool)
        print(f"Added tool to db: {tool["name"]}")

    result = tool_search.invoke(
        query="Get me employees having salary > 30000 in engineering department.",
        k=3,
        TOOLS=TOOLS,
    )

    print(result.tools)
    print(result.tools_callable)
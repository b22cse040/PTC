import json
import sqlite3
from dataclasses import dataclass
from typing import Any, Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer

from src.tools.tool_executors import TOOL_EXECUTORS
from src.tool_search_module.tool_executor import ToolExecutor


@dataclass
class ToolSearchResult:
    tools: List[Dict[str, Any]]
    tool_executors: Dict[str, ToolExecutor]


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
                source TEXT NOT NULL,
                input_schema TEXT NOT NULL,
                output_schema TEXT NOT NULL,
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

    def add_tool(
        self,
        tool: Dict[str, Any],
    ) -> None:
        """
        Add a tool to the database only if it does not already exist.

        The embedding is generated only from:

            [CLS] tool[name] [SEP] tool[description]
        """

        name = tool["name"]

        existing_tool = self.db.execute(
            """
            SELECT id
            FROM tools
            WHERE name = ?
            """,
            (name,),
        ).fetchone()

        if existing_tool is not None:
            return

        description = tool["description"]

        embedding_text = (
            f"[CLS] tool[{name}] [SEP] tool[{description}]"
        )

        embedding = self.model.encode(
            embedding_text,
            normalize_embeddings=True,
        )

        cursor = self.db.execute(
            """
            INSERT INTO tools (
                name,
                description,
                source,
                input_schema,
                output_schema,
                input_example
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                description,
                tool["source"],
                json.dumps(tool["input-schema"]),
                json.dumps(tool["output_schema"]),
                json.dumps(tool["input_example"]),
            ),
        )

        tool_id = cursor.lastrowid

        self.db.execute(
            """
            INSERT INTO tool_embeddings (
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
                t.source,
                t.input_schema,
                t.output_schema,
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

            score = float(
                np.dot(query_embedding, embedding)
            )

            output_schema = json.loads(
                row["output_schema"]
            )

            enriched_description = (
                f"{row['description']}\n\n"
                f"Output schema:\n"
                f"{json.dumps(output_schema, indent=2)}"
            )

            results.append(
                {
                    "tool_id": row["id"],
                    "name": row["name"],
                    "description": enriched_description,
                    "source": row["source"],
                    "input_schema": json.loads(
                        row["input_schema"]
                    ),
                    "output_schema": output_schema,
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

    def get_tool_executors(
        self,
        result_search_tools: List[Dict[str, Any]],
    ) -> Dict[str, ToolExecutor]:

        tool_executors: Dict[str, ToolExecutor] = {}

        for tool in result_search_tools:
            tool_name = tool["name"]

            if tool_name not in TOOL_EXECUTORS:
                raise KeyError(
                    f"Tool '{tool_name}' exists in the database "
                    f"but is missing from TOOL_EXECUTORS."
                )

            tool_executors[tool_name] = (
                TOOL_EXECUTORS[tool_name]
            )

        return tool_executors

    def invoke(
        self,
        query: str,
        k: int,
    ) -> ToolSearchResult:

        tools = self.search_tools(
            query=query,
            k=k,
        )

        tool_executors = self.get_tool_executors(
            result_search_tools=tools,
        )

        return ToolSearchResult(
            tools=tools,
            tool_executors=tool_executors,
        )

    def close(self) -> None:
        self.db.close()

if __name__ == "__main__":
    from src.tools.tool_definitions import TOOL_DEFINITIONS
    tool_search = ToolSearchModule(
        db_path="tools.db",
    )

    for tool in TOOL_DEFINITIONS:
        tool_search.add_tool(tool)
        print(f"Tool {tool["name"]} added")

    result = tool_search.invoke(
        query="Get me employees from the engineering department.",
        k=3,
    )

    print("Tools:")
    for tool in result.tools:
        print(tool)

    print("\nTool Executors:")
    for name, executor in result.tool_executors.items():
        print(f"{name}: {type(executor).__name__}")

    tool_search.close()
"""
Query Engine Module
Converts natural language to Pandas code using Gemini API
"""

from google import genai
import pandas as pd
import re
from data_loader import get_schema_description


class QueryEngine:
    def __init__(self, api_key, df):
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash-lite'
        self.df = df
        self.schema = get_schema_description(df)

    def _generate_code(self, question):
        prompt = f"""You are a Python Pandas expert. Convert this question into Pandas code.

{self.schema}

Rules:
1. DataFrame is already loaded as 'df'
2. Return ONLY Python code, no explanations
3. Store result in variable called 'result'
4. No markdown formatting or code blocks
5. No print statements

Question: {question}

Python Code:"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        code = response.text.strip()
        code = re.sub(r'^```python\s*', '', code)
        code = re.sub(r'^```\s*', '', code)
        code = re.sub(r'\s*```$', '', code)
        return code

    def _run_code(self, code):
        try:
            local_vars = {'pd': pd, 'df': self.df.copy()}
            exec(code, local_vars)
            return True, local_vars.get('result', 'No result'), ""
        except Exception as e:
            return False, None, str(e)

    def _format_result(self, result):
        if isinstance(result, pd.DataFrame):
            if len(result) == 0:
                return "No records found."
            elif len(result) <= 20:
                return result.to_string(index=False)
            else:
                return result.head(20).to_string(index=False)
        elif isinstance(result, pd.Series):
            return result.to_string()
        elif isinstance(result, (int, float)):
            return f"{result:,}" if isinstance(result, int) else f"{result:,.2f}"
        else:
            return str(result)

    def _get_summary(self, result, question):
        try:
            prompt = f"Question: {question}\nResult: {str(result)[:1000]}\nGive a 1 sentence summary:"
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except:
            return ""

    def query(self, question):
        code = self._generate_code(question)
        success, result, error = self._run_code(code)

        if not success:
            # Retry once
            code = self._generate_code(f"{question} (Previous error: {error})")
            success, result, error = self._run_code(code)

        if success:
            return {
                'success': True,
                'answer': self._format_result(result),
                'summary': self._get_summary(result, question),
                'code': code
            }
        else:
            return {
                'success': False,
                'answer': f"Error: {error}",
                'summary': "",
                'code': code
            }


def create_query_engine(api_key, df):
    return QueryEngine(api_key, df)

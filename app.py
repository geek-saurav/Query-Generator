import streamlit as st
import google.generativeai as genai


GOOGLE_API_KEY = "AIzaSyDIELMQBsa0LB_dDTd3K1oDZeo_jZ7vbMs"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def main():
    st.set_page_config(page_title="SQL query generator ",page_icon=":robot:")
    st.markdown(
        """
            <div style="background-color: #9B7EBD; padding: 40px; border-radius: 10px; text-align: center; color: white; margin-bottom: 20px; box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2);">
                <h1 style="font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">SQL Query Generator 🚀 📊 🔍</h1>
                <h3 style="font-size: 1.5em; margin-bottom: 20px;">Generate SQL queries effortlessly with explanations!</h3>
                <p style="font-size: 1.2em;">This tool allows you to create SQL queries based on your input, along with explanations and sample output.</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    text_input = st.text_area("Enter your query here.")
    
    submit = st.button('Generate sql query')

    if submit:
        with st.spinner("generative sql qury..."):
            template = """
                Create a SQL query snippet using the below text:
                ```
                    {text_input}
                ```
                I just want a SQL query.

            """
            forward_template = template.format(text_input=text_input)

            response = model.generate_content(forward_template)
            sql_query=response.text

            sql_query = sql_query.strip().lstrip("```sql").rstrip("```")

            expected_output = """
                what would be the expected response of this SQL query snippet:
                ```
                    {sql_query}
                ```
                provide sample tabular Response with no explanation.

            """

            expected_output_formatted = expected_output.format(sql_query=sql_query)
            output1 = model.generate_content(expected_output_formatted)
            output1 = output1.text


            explanation = """
                Explain this SQL query :
                ```
                    {sql_query}
                ```
                please provide with simplest explanation.

            """

            explanation_formatted = explanation.format(sql_query=sql_query)
            explanation=model.generate_content(explanation_formatted)
            explanation = explanation.text


            with st.container():
                st.success("SQL Query Generated Sucessfully! Here is your Query Below!")
                st.code(sql_query,language="sql")

                st.success("Expected output of this sql query will be")
                st.markdown(output1)

                st.success("explaination of this SQL Query:")
                st.markdown(explanation)


        

main()
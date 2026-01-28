import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Brutal Startup Idea Validator",
    page_icon="💡",
    layout="wide"
)

# Get API key from environment
os.environ['GROQ_API_KEY']= os.getenv('GROQ_API_KEY')

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'startup_context' not in st.session_state:
    st.session_state.startup_context = ""

# Title and description
st.title("💡 Brutal Startup Idea Validator")
st.markdown("### Get an honest, no-BS analysis of your startup idea")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    brutality_level = st.slider(
        "Brutality Level",
        min_value=1,
        max_value=10,
        value=7,
        help="How harsh should the feedback be? (1=gentle, 10=savage)"
    )
    
    st.markdown("---")
    
    # Additional context inputs
    st.subheader("📋 Optional Details")
    target_market = st.text_input("Target Market", placeholder="e.g., Urban millennials")
    budget_range = st.text_input("Budget Range", placeholder="e.g., $10K-$50K")
    timeline = st.text_input("Timeline", placeholder="e.g., 6 months to MVP")
    
    st.markdown("---")
    st.markdown("### About")
    st.info("This tool provides a brutally honest analysis of your startup idea using AI.")
    st.markdown("### Features")
    st.markdown("""
    - ✅ Idea Validation
    - 📊 Market Analysis
    - 💰 Investment Requirements
    - 📈 Future Scope
    - ⚠️ Risks & Challenges
    - 💬 Follow-up Questions
    """)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input validation prompt template - checks if it's a startup idea
validation_template = """You are a strict input validator. Determine if the user's input is a NEW STARTUP IDEA or something else.

USER INPUT: {user_input}

Respond with ONLY ONE WORD:
- "STARTUP" - if this is clearly a NEW startup idea, business concept, or entrepreneurial proposal
- "OTHER" - if this is a follow-up question, clarification, or anything else

Examples of STARTUP:
- "An app that helps people find parking spots"
- "A service connecting freelance designers with small businesses"
- "Subscription box for organic pet food"

Examples of OTHER (follow-up questions or general queries):
- "Can you explain the revenue model more?"
- "What about marketing?"
- "How do I reduce the risks?"
- "Tell me more about investment"
- "What is a startup?"
- "Hello"

Respond with ONLY: STARTUP or OTHER"""

# Initial startup analysis prompt
initial_analysis_template = """You are a brutal, experienced startup advisor with 20+ years of experience. You've seen thousands of startups fail and succeed. Your job is to provide HONEST, DIRECT feedback without sugar-coating anything.

Analyze this startup idea with a brutality level of {brutality_level}/10:

STARTUP IDEA: {startup_idea}

TARGET MARKET: {target_market}
BUDGET RANGE: {budget_range}
TIMELINE: {timeline}

Provide a comprehensive analysis in the following format:

## 🎯 IDEA VALIDATION (Valid/Invalid)
State clearly if this idea is VALID or INVALID. Be direct about fatal flaws.

## 📊 SHORT-TERM GOALS (0-6 months)
List 3-5 realistic short-term goals. Be specific and actionable.

## 🎯 LONG-TERM GOALS (1-3 years)
List 3-5 long-term strategic goals. Think big but realistic.

## 💰 INVESTMENT REQUIRED
Break down:
- Initial Investment: $X - $Y
- Monthly Burn Rate: $X - $Y
- Total 1st Year: $X - $Y

Be specific with numbers based on the idea.

## 📈 REVENUE POTENTIAL
- Can you sell this? YES/NO (with brutal honesty)
- Expected timeline to first sale: X months
- Revenue potential (Year 1, Year 2, Year 3)
- Realistic exit opportunities (if any)

## ⚖️ RISK ANALYSIS
### LOSSES (Be brutal about what can go wrong)
- List 4-6 major risks and potential losses
- Include realistic failure scenarios

### BENEFITS (Don't oversell, be realistic)
- List 3-5 genuine benefits if successful
- Include competitive advantages (if any exist)

## 🚀 FUTURE SCOPE
- Scalability potential (Low/Medium/High)
- Market trends supporting/opposing this idea
- Evolution opportunities

## 💡 BRUTAL IMPROVEMENTS
List 5-7 specific, actionable improvements. Don't hold back on what's wrong and how to fix it.

## 🎯 FINAL VERDICT
Give a percentage score (0-100%) for:
- Viability: X%
- Profitability: X%
- Scalability: X%
- Overall Score: X%

End with a ONE-SENTENCE brutal truth about this idea.

Remember: Be HONEST, be DIRECT, be BRUTAL (level {brutality_level}/10). No false hope, no generic advice."""

# Follow-up conversation template
followup_template = """You are a brutal, experienced startup advisor. You are continuing a conversation about a startup idea.

PREVIOUS CONVERSATION CONTEXT:
{conversation_history}

STARTUP CONTEXT:
{startup_context}

USER'S FOLLOW-UP QUESTION: {user_question}

BRUTALITY LEVEL: {brutality_level}/10

Provide a focused, honest answer to their question. Reference the previous analysis when relevant. Stay brutal but helpful. If they ask something unrelated to startup validation, politely redirect them to focus on their startup idea.

Keep your response concise but comprehensive. Use the same brutal, direct tone as before."""

# Function to get conversation history
def get_conversation_history():
    history = ""
    for msg in st.session_state.messages[-6:]:  # Last 6 messages (3 exchanges)
        if msg["role"] == "user":
            history += f"\nUser: {msg['content']}\n"
        else:
            history += f"Assistant: {msg['content'][:500]}...\n"  # Truncate long responses
    return history

# Chat input at the bottom (ChatGPT style)
if prompt := st.chat_input("Describe your startup idea..."):
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response with streaming
    with st.chat_message("assistant"):
        try:
            # Initialize LLM
            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                streaming=True
            )
            
            # Determine if this is a new startup idea or follow-up
            llm_validator = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.3
            )
            
            validation_prompt = PromptTemplate(
                input_variables=["user_input"],
                template=validation_template
            )
            
            formatted_validation = validation_prompt.format(user_input=prompt)
            validation_result = llm_validator.invoke(formatted_validation).content.strip().upper()
            
            message_placeholder = st.empty()
            full_response = ""
            
            # Handle based on input type
            if "STARTUP" in validation_result:
                # This is a new startup idea - do full analysis
                st.session_state.startup_context = prompt  # Save the startup context
                
                analysis_prompt = PromptTemplate(
                    input_variables=["startup_idea", "target_market", "budget_range", "timeline", "brutality_level"],
                    template=initial_analysis_template
                )
                
                formatted_analysis = analysis_prompt.format(
                    startup_idea=prompt,
                    target_market=target_market if target_market else "Not specified",
                    budget_range=budget_range if budget_range else "Not specified",
                    timeline=timeline if timeline else "Not specified",
                    brutality_level=brutality_level
                )
                
                # Stream the response
                for chunk in llm.stream(formatted_analysis):
                    full_response += chunk.content
                    message_placeholder.markdown(full_response + "▌")
                
            else:
                # This is a follow-up question
                if not st.session_state.startup_context:
                    # No previous startup context
                    full_response = """❓ **No Startup Idea Found**

I don't see any startup idea in our conversation yet. Please first describe your startup idea, and then I can answer your questions about it.

**Example:** "A mobile app that connects local farmers directly with consumers for fresh produce delivery."
"""
                    message_placeholder.markdown(full_response)
                else:
                    # Answer the follow-up question
                    followup_prompt = PromptTemplate(
                        input_variables=["conversation_history", "startup_context", "user_question", "brutality_level"],
                        template=followup_template
                    )
                    
                    formatted_followup = followup_prompt.format(
                        conversation_history=get_conversation_history(),
                        startup_context=st.session_state.startup_context,
                        user_question=prompt,
                        brutality_level=brutality_level
                    )
                    
                    # Stream the response
                    for chunk in llm.stream(formatted_followup):
                        full_response += chunk.content
                        message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"❌ **Error occurred:** {str(e)}\n\n💡 **Troubleshooting Tips:**\n- Check your internet connection\n- Try restarting the application"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Add some spacing before footer
st.markdown("<br>" * 3, unsafe_allow_html=True)

# Footer - Fixed at bottom
# st.markdown("""
# <style>
#     .footer {
#         position: fixed;
#         left: 0;
#         bottom: 0;
#         width: 100%;
#         background-color: #0E1117;
#         color: #808495;
#         text-align: center;
#         padding: 10px 0;
#         font-size: 14px;
#         z-index: 999;
#         border-top: 1px solid #262730;
#     }
#     /* Add padding to main content to prevent overlap with fixed footer */
#     .main .block-container {
#         padding-bottom: 80px;
#     }
# </style>
# <div class="footer">
#     <p>Built with ❤️ using Streamlit, LangChain & Groq | ⚠️ AI-generated advice - Always do your own research</p>
# </div>
# """, unsafe_allow_html=True)
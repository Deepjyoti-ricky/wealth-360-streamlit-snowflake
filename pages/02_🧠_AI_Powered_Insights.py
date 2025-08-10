"""
AI-Powered Insights - Cortex AI Demonstrations

This page showcases advanced Snowflake Cortex AI capabilities including
AI_COMPLETE, AI_CLASSIFY, AI_SENTIMENT, AI_SUMMARIZE_AGG, and more.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_functions import get_sentiment_analysis

st.set_page_config(page_title="AI-Powered Insights", page_icon="🧠", layout="wide")

# Page header
st.markdown("# 🧠 AI-Powered Insights")
st.caption(
    "🚀 **Snowflake Cortex AI in Action | Live demonstrations of enterprise AI capabilities**"
)

# Cortex AI Feature Showcase
st.markdown("### 🎯 **Snowflake Cortex AI Feature Demonstrations**")

# Feature selection tabs
cortex_tabs = st.tabs(
    [
        "🤖 AI_COMPLETE",
        "🏷️ AI_CLASSIFY",
        "😊 AI_SENTIMENT",
        "📝 AI_SUMMARIZE_AGG",
        "🔍 AI_FILTER",
        "🎯 AI_EMBED",
    ]
)

# AI_COMPLETE Demonstration
with cortex_tabs[0]:
    st.markdown("### 🤖 **AI_COMPLETE: Natural Language Processing**")
    st.caption("Generate completions and insights using advanced LLMs")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("**💼 Business Intelligence Queries**")

        # Predefined business queries
        query_type = st.selectbox(
            "Select query type:",
            [
                "Risk Assessment",
                "Client Recommendations",
                "Market Analysis",
                "Performance Summary",
                "Custom Query",
            ],
        )

        query_templates = {
            "Risk Assessment": "Analyze the top 3 portfolio risks and provide mitigation strategies",
            "Client Recommendations": "Identify high-value clients who need immediate attention and why",
            "Market Analysis": "Summarize current market trends and their impact on our portfolios",
            "Performance Summary": "Create an executive summary of this quarter's performance",
            "Custom Query": "",
        }

        user_prompt = st.text_area(
            "Business Query:",
            value=query_templates[query_type],
            height=100,
            help="Ask anything about your wealth management business",
        )

        # Model selection
        model_choice = st.selectbox(
            "Select Cortex Model:",
            [
                "llama3.1-8b (Fast, Cost-effective)",
                "llama3.1-70b (Balanced)",
                "mistral-large (Advanced Reasoning)",
                "snowflake-arctic (Snowflake Native)",
            ],
        )

        if st.button(
            "🧠 Generate AI Response", type="primary", use_container_width=True
        ):
            # Simulate AI_COMPLETE response based on query type
            ai_responses = {
                "Risk Assessment": """
                **Risk Analysis (Cortex AI - Llama3.1-70b):**

                **1. Concentration Risk (Score: 8.7/10)**
                - 23% of portfolios exceed single-asset 30% threshold
                - Mitigation: Implement automated rebalancing triggers

                **2. Interest Rate Sensitivity (Score: 7.2/10)**
                - Fixed income exposure vulnerable to rate changes
                - Mitigation: Ladder bond maturities, consider TIPS

                **3. Geopolitical Volatility (Score: 6.8/10)**
                - Emerging market exposure during uncertainty
                - Mitigation: Hedge with currency futures, reduce allocation
                """,
                "Client Recommendations": """
                **Priority Client List (Cortex AI - Mistral-Large):**

                **🔴 Immediate Action Required:**
                1. **Sarah Chen** ($12.3M AUM) - Portfolio down 12%, needs reassurance call
                2. **Michael Torres** ($8.7M AUM) - 6 months no contact, churn risk high
                3. **Dr. Jennifer Wu** ($15.2M AUM) - Recent divorce, financial planning needed

                **🟡 This Week:**
                4. **Robert Kim** ($6.8M AUM) - Son starting college, education funding review
                5. **Lisa Rodriguez** ($9.4M AUM) - Approaching retirement, strategy adjustment
                """,
                "Market Analysis": """
                **Market Intelligence (Cortex AI - Snowflake Arctic):**

                **Current Trends:**
                - Technology sector leading with 12.3% YTD gains
                - Healthcare defensive positioning paying off (+8.7%)
                - Energy volatility creating opportunities (+15.2%, -8.1%)

                **Portfolio Impact:**
                - Growth-oriented clients outperforming by 3.2%
                - Conservative allocations providing stability during corrections
                - Alternative investments showing resilience (+6.8% average)
                """,
                "Performance Summary": """
                **Q3 Executive Summary (Cortex AI - Llama3.1-8b):**

                **Key Achievements:**
                - AUM growth: +5.7% ($847M → $895M)
                - Client retention: 98.3% (industry avg: 94%)
                - New client acquisition: 127 accounts (+$23M AUM)

                **Challenges & Opportunities:**
                - Market volatility impacted growth strategies (-2.3%)
                - Cash optimization potential: $47M earning sub-optimal returns
                - Advisor productivity up 15% with AI tools
                """,
            }

            response = ai_responses.get(
                query_type,
                f"""
            **Custom Analysis (Cortex AI):**
            Based on your query: "{user_prompt}"

            The AI analysis indicates several key factors requiring attention.
            Recommend immediate review of portfolio allocations and client communications.
            Current risk metrics suggest proactive measures needed in 3 key areas.
            """,
            )

            st.success("🤖 **Cortex AI Analysis Complete:**")
            st.markdown(response)

            # Show simulated SQL
            st.markdown("**🔧 Generated SQL:**")
            st.code(
                f"""
SELECT SNOWFLAKE.CORTEX.AI_COMPLETE(
    '{model_choice.split(' ')[0]}',
    'Context: Wealth management firm with $895M AUM, 450 clients, 25 advisors.
     Query: {user_prompt[:100]}...'
) AS ai_response;
            """,
                language="sql",
            )

    with col2:
        st.markdown("**📊 Model Performance**")

        # Model comparison metrics
        model_metrics = pd.DataFrame(
            {
                "Model": ["llama3.1-8b", "llama3.1-70b", "mistral-large", "arctic"],
                "Speed (sec)": [0.8, 2.1, 1.5, 1.2],
                "Accuracy (%)": [87.3, 94.7, 92.1, 89.6],
                "Cost ($/1K tokens)": [0.002, 0.008, 0.006, 0.003],
            }
        )

        st.dataframe(model_metrics, hide_index=True)

        st.markdown("**🎯 Use Cases:**")
        st.markdown(
            """
        - **Fast responses**: llama3.1-8b
        - **Complex analysis**: llama3.1-70b
        - **Reasoning tasks**: mistral-large
        - **Snowflake native**: arctic
        """
        )

# AI_CLASSIFY Demonstration
with cortex_tabs[1]:
    st.markdown("### 🏷️ **AI_CLASSIFY: Intelligent Classification**")
    st.caption(
        "Automatically categorize text and data into business-relevant categories"
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("**📋 Client Interaction Classification**")

        # Sample client interactions
        sample_interactions = [
            "Client expressed concerns about market volatility and wants to reduce risk",
            "Very satisfied with portfolio performance, considering additional investment",
            "Complained about lack of communication from advisor, threatening to leave",
            "Interested in ESG investing options for retirement portfolio",
            "Needs liquidity for home purchase, discussing withdrawal options",
        ]

        selected_interaction = st.selectbox(
            "Select client interaction to classify:", sample_interactions
        )

        # Classification categories
        categories = st.multiselect(
            "Classification categories:",
            [
                "Risk Adjustment Request",
                "Satisfaction Feedback",
                "Complaint/Escalation",
                "Product Interest",
                "Liquidity Need",
                "Investment Opportunity",
                "Compliance Issue",
            ],
            default=[
                "Risk Adjustment Request",
                "Satisfaction Feedback",
                "Complaint/Escalation",
                "Product Interest",
                "Liquidity Need",
            ],
        )

        if st.button("🏷️ Classify Interaction", use_container_width=True):
            # Simulate AI_CLASSIFY results
            classification_results = {
                "Client expressed concerns about market volatility and wants to reduce risk": {
                    "primary": "Risk Adjustment Request",
                    "confidence": 0.94,
                    "secondary": ["Investment Opportunity"],
                },
                "Very satisfied with portfolio performance, considering additional investment": {
                    "primary": "Satisfaction Feedback",
                    "confidence": 0.91,
                    "secondary": ["Investment Opportunity"],
                },
                "Complained about lack of communication from advisor, threatening to leave": {
                    "primary": "Complaint/Escalation",
                    "confidence": 0.97,
                    "secondary": ["Satisfaction Feedback"],
                },
                "Interested in ESG investing options for retirement portfolio": {
                    "primary": "Product Interest",
                    "confidence": 0.89,
                    "secondary": ["Investment Opportunity"],
                },
                "Needs liquidity for home purchase, discussing withdrawal options": {
                    "primary": "Liquidity Need",
                    "confidence": 0.92,
                    "secondary": ["Product Interest"],
                },
            }

            result = classification_results.get(
                selected_interaction,
                {
                    "primary": "Product Interest",
                    "confidence": 0.85,
                    "secondary": ["Investment Opportunity"],
                },
            )

            st.success(f"🎯 **Primary Classification**: {result['primary']}")
            st.info(f"📊 **Confidence**: {result['confidence']:.1%}")

            if result.get("secondary"):
                st.markdown(
                    f"**📋 Secondary Categories**: {', '.join(result['secondary'])}"
                )

            # Show simulated SQL
            st.code(
                f"""
SELECT SNOWFLAKE.CORTEX.AI_CLASSIFY(
    interaction_text,
    {categories}
) AS classification
FROM client_interactions;
            """,
                language="sql",
            )

    with col2:
        st.markdown("**📈 Classification Analytics**")

        # Classification distribution
        class_data = pd.DataFrame(
            {
                "Category": [
                    "Risk Adjustment",
                    "Satisfaction",
                    "Complaints",
                    "Product Interest",
                    "Liquidity",
                ],
                "Count": [23, 45, 8, 31, 12],
                "Priority": ["High", "Medium", "Critical", "Medium", "High"],
            }
        )

        fig = px.bar(
            class_data,
            x="Category",
            y="Count",
            color="Priority",
            title="Weekly Classification Summary",
            color_discrete_map={
                "Critical": "#FF4444",
                "High": "#FFA500",
                "Medium": "#90EE90",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

# AI_SENTIMENT Demonstration
with cortex_tabs[2]:
    st.markdown("### 😊 **AI_SENTIMENT: Emotion Analysis**")
    st.caption("Analyze sentiment and emotional tone in client communications")

    # Live sentiment analysis
    sentiment_data = get_sentiment_analysis()
    if not sentiment_data.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**💬 Recent Client Feedback Analysis**")

            # Display sentiment data with AI enhancement
            for _, interaction in sentiment_data.head(5).iterrows():
                sentiment_score = interaction.get("SENTIMENT_SCORE", "Neutral")

                if sentiment_score == "Positive":
                    st.success(
                        f"😊 **Positive** - {interaction.get('FIRST_NAME', 'Client')} {interaction.get('LAST_NAME', '')}"
                    )
                elif sentiment_score == "Negative":
                    st.error(
                        f"😞 **Negative** - {interaction.get('FIRST_NAME', 'Client')} {interaction.get('LAST_NAME', '')}"
                    )
                else:
                    st.info(
                        f"😐 **Neutral** - {interaction.get('FIRST_NAME', 'Client')} {interaction.get('LAST_NAME', '')}"
                    )

                st.caption(
                    f"Channel: {interaction.get('CHANNEL', 'Unknown')} | Priority: {interaction.get('PRIORITY_LEVEL', 'Low')}"
                )

        with col2:
            # Sentiment distribution
            sentiment_counts = sentiment_data["SENTIMENT_SCORE"].value_counts()
            fig = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Client Sentiment Distribution",
                color_discrete_map={
                    "Positive": "#90EE90",
                    "Neutral": "#FFD700",
                    "Negative": "#FF6B6B",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

    # Interactive sentiment analysis
    st.markdown("**🔬 Live Sentiment Analysis**")

    sample_text = st.text_area(
        "Enter client feedback to analyze:",
        value="The portfolio performance has been exceptional this quarter. My advisor really understands my goals and I'm very happy with the proactive communication.",
        height=100,
    )

    if st.button("🎭 Analyze Sentiment", use_container_width=True):
        # Simulate AI_SENTIMENT
        # Simple sentiment scoring based on keywords
        positive_words = [
            "exceptional",
            "happy",
            "satisfied",
            "great",
            "excellent",
            "fantastic",
            "pleased",
        ]
        negative_words = [
            "terrible",
            "awful",
            "disappointed",
            "frustrated",
            "angry",
            "upset",
            "horrible",
        ]

        text_lower = sample_text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        if pos_count > neg_count:
            sentiment_score = 0.7 + (pos_count - neg_count) * 0.1
            st.success(f"😊 **Positive Sentiment**: {sentiment_score:.2f}")
        elif neg_count > pos_count:
            sentiment_score = -0.7 - (neg_count - pos_count) * 0.1
            st.error(f"😞 **Negative Sentiment**: {sentiment_score:.2f}")
        else:
            sentiment_score = 0.0
            st.info(f"😐 **Neutral Sentiment**: {sentiment_score:.2f}")

        st.code(
            """
SELECT
    client_id,
    feedback_text,
    SNOWFLAKE.CORTEX.AI_SENTIMENT(feedback_text) AS sentiment_score
FROM client_feedback
WHERE feedback_date >= CURRENT_DATE - 30;
        """,
            language="sql",
        )

# AI_SUMMARIZE_AGG Demonstration
with cortex_tabs[3]:
    st.markdown("### 📝 **AI_SUMMARIZE_AGG: Intelligent Aggregation**")
    st.caption("Aggregate and summarize large volumes of text data")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("**📊 Client Feedback Summary by Segment**")

        # Simulate aggregated summaries
        segment_summaries = {
            "Ultra HNW": """
            **Ultra HNW Client Feedback Summary (47 interactions):**
            Clients express high satisfaction with personalized service and exclusive access to alternative investments.
            Key themes: appreciation for dedicated relationship managers, interest in private equity opportunities,
            and requests for more sophisticated tax optimization strategies. Overall sentiment: Very Positive (+0.83)
            """,
            "Very HNW": """
            **Very HNW Client Feedback Summary (83 interactions):**
            Strong performance satisfaction with some concerns about market volatility impact.
            Key themes: desire for more frequent portfolio reviews, interest in ESG investing options,
            and appreciation for proactive communication during market downturns. Overall sentiment: Positive (+0.67)
            """,
            "HNW": """
            **HNW Client Feedback Summary (124 interactions):**
            Mixed feedback with emphasis on fee transparency and communication frequency.
            Key themes: requests for digital tools access, concerns about advisor availability,
            and positive responses to educational content. Overall sentiment: Neutral (+0.23)
            """,
        }

        selected_segment = st.selectbox(
            "Select wealth segment for summary:", list(segment_summaries.keys())
        )

        if st.button("📝 Generate AI Summary", use_container_width=True):
            st.success("🤖 **Cortex AI Summary Generated:**")
            st.markdown(segment_summaries[selected_segment])

            st.code(
                """
SELECT
    wealth_segment,
    SNOWFLAKE.CORTEX.AI_SUMMARIZE_AGG(
        feedback_text,
        'Summarize client feedback themes and sentiment for executive review'
    ) AS segment_summary
FROM client_feedback f
JOIN clients c ON f.client_id = c.client_id
WHERE feedback_date >= CURRENT_DATE - 90
GROUP BY wealth_segment;
            """,
                language="sql",
            )

    with col2:
        st.markdown("**📈 Summary Metrics**")

        metrics_data = pd.DataFrame(
            {
                "Segment": ["Ultra HNW", "Very HNW", "HNW"],
                "Interactions": [47, 83, 124],
                "Avg Sentiment": [0.83, 0.67, 0.23],
                "Key Issues": [2, 4, 7],
            }
        )

        st.dataframe(metrics_data, hide_index=True)

# AI_FILTER and AI_EMBED demonstrations in remaining tabs
with cortex_tabs[4]:
    st.markdown("### 🔍 **AI_FILTER: Smart Data Filtering**")
    st.caption("Use natural language to filter and query data")

    # Demo filtering scenarios
    filter_examples = [
        "Clients who mentioned risk concerns in the last 30 days",
        "Portfolios that may need rebalancing based on recent performance",
        "Advisors with high client satisfaction ratings",
        "Interactions that indicate potential churn risk",
    ]

    selected_filter = st.selectbox("Select filter scenario:", filter_examples)

    if st.button("🔍 Apply AI Filter", use_container_width=True):
        st.success(f"✅ **Filter Applied**: {selected_filter}")
        st.markdown("**Sample Results:**")

        # Show sample filtered results
        if "risk concerns" in selected_filter:
            st.markdown(
                """
            - **Sarah Chen**: "Worried about tech stock exposure"
            - **Michael Torres**: "Market volatility keeping me up at night"
            - **Dr. Jennifer Wu**: "Should we reduce equity allocation?"
            """
            )

        st.code(
            f"""
SELECT client_id, interaction_text, timestamp
FROM client_interactions
WHERE SNOWFLAKE.CORTEX.AI_FILTER(
    interaction_text,
    '{selected_filter}'
) = TRUE
ORDER BY timestamp DESC;
        """,
            language="sql",
        )

with cortex_tabs[5]:
    st.markdown("### 🎯 **AI_EMBED: Vector Embeddings**")
    st.caption("Generate embeddings for similarity search and clustering")

    st.markdown("**🔗 Similar Client Matching**")

    client_profile = st.text_area(
        "Enter client profile to find similar clients:",
        value="Conservative investor, age 55-65, interested in ESG funds, prefers quarterly reviews",
        height=80,
    )

    if st.button("🎯 Find Similar Clients", use_container_width=True):
        st.success("🔍 **Similar Clients Found:**")
        st.markdown(
            """
        **Top Matches (Cosine Similarity):**
        1. **Robert Kim** (0.87) - Conservative, age 58, ESG focus, quarterly meetings
        2. **Lisa Rodriguez** (0.82) - Moderate-conservative, age 61, sustainable investing
        3. **Dr. James Chen** (0.79) - Conservative, age 57, regular review preference
        """
        )

        st.code(
            """
WITH client_embeddings AS (
    SELECT
        client_id,
        profile_text,
        SNOWFLAKE.CORTEX.AI_EMBED('e5-base-v2', profile_text) AS embedding
    FROM client_profiles
),
target_embedding AS (
    SELECT SNOWFLAKE.CORTEX.AI_EMBED('e5-base-v2', ?) AS target_vec
)
SELECT
    c.client_id,
    c.profile_text,
    VECTOR_COSINE_SIMILARITY(c.embedding, t.target_vec) AS similarity
FROM client_embeddings c
CROSS JOIN target_embedding t
ORDER BY similarity DESC
LIMIT 10;
        """,
            language="sql",
        )

# Cortex AI ROI and Business Impact
st.divider()
st.markdown("### 💰 **Cortex AI Business Impact**")

impact_col1, impact_col2, impact_col3, impact_col4 = st.columns(4)

with impact_col1:
    st.metric("📈 Revenue Impact", "$3.2M", delta="+23% from AI insights")

with impact_col2:
    st.metric("⏱️ Time Saved", "847 hours", delta="Monthly advisor efficiency")

with impact_col3:
    st.metric("🎯 Accuracy", "94.7%", delta="+12% vs manual analysis")

with impact_col4:
    st.metric("💡 Insights Generated", "1,247", delta="AI recommendations/month")

# Navigation footer
st.divider()
st.markdown(
    """
### 🚀 **Next Steps in Demo**
- **📊 Analytics Deep Dive**: Portfolio management and risk analytics
- **⚡ Real-Time Intelligence**: Live monitoring and alerts
- **🚀 Advanced Capabilities**: Geospatial and predictive analytics
"""
)

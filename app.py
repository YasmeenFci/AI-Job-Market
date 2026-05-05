import streamlit as st
from models.AI_jobs import df 
import plotly.graph_objects as go
import plotly.express as px
st.set_page_config(layout='wide')
st.markdown(
    """
    <div style="
        background-color:#1e1e1e;
        padding:12px;
        border-radius:15px;
        text-align:left;
        box-shadow:0px 2px 8px rgba(0,0,0,0.4);
        margin-bottom:20px;
    ">
        <h2 style="color:white;margin:0;">
            AI Job Market  <Italic style="color:#4DA6FF;"> (Interactive Dashboard)</span>
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)
card1,card2,card3,card4=st.columns([0.25,0.25,0.25,0.25])

total_jobs=df.groupby('year')['job_openings'].sum()[2026]
avg_salary=df['salary_usd'].mean()
top_role=df.groupby('job_role')['job_openings'].sum().sort_values().index[-1]
df_2026=df[df['year']==2026]
top_country=df_2026.groupby('country')['job_openings'].sum().sort_values().index[-1]
with card1:
    st.markdown(
        f"""
        <div style="
            background-color:#1e1e1e;
            height:90px;
            padding:5px;
            border-radius:10px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
        ">
        <div style="color:white;font-size:20px;margin:0;">
            Total Job Openings (2026)
    </div>
    <div style="color:#4DA6FF;font-size:20px;font-weight:bold;margin-top:4px;">
        {total_jobs:,}
    </div>
</div>
            """,
            unsafe_allow_html=True
        )

with card2:
    st.markdown(
        f"""
        <div style="
            background-color:#1e1e1e;
            height:90px;
            padding:5px;
            border-radius:10px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
        ">
        <div style="color:white;font-size:20px;margin:0;">
            AVG.Salary (USD)
    </div>
    <div style="color:#4DA6FF;font-size:20px;font-weight:bold;margin-top:4px;">
        ${int(avg_salary):,}
    </div>
</div>
            """,
            unsafe_allow_html=True
        )
with card3:
    st.markdown(
        f"""
        <div style="
            background-color:#1e1e1e;
            height:90px;
            padding:5px;
            border-radius:10px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
        ">
        <div style="color:white;font-size:20px;margin:0;">
            Top Role (Hiring)
    </div>
    <div style="color:#4DA6FF;font-size:20px;font-weight:bold;margin-top:4px;">
        {top_role}
    </div>
</div>
            """,
            unsafe_allow_html=True
        )
with card4:
    st.markdown(
        f"""
        <div style="
            background-color:#1e1e1e;
            height:90px;
            padding:5px;
            border-radius:10px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
        ">
        <div style="color:white;font-size:20px;margin:0;">
            Top AI Hiring Countries (2026)
    </div>
    <div style="color:#4DA6FF;font-size:20px;font-weight:bold;margin-top:4px;">
        {top_country}
    </div>
</div>
            """,
            unsafe_allow_html=True
        )
colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2"]

fig = go.Figure()
roles = df.groupby('job_role')['salary_usd'].mean().sort_values(ascending=False).head(5).index
df_clean = df.groupby(["job_role", "year"], as_index=False)["salary_usd"].mean()
df_layoff=df.groupby('year',as_index=False)['layoff_risk'].sum().sort_values('year')
for i, role in enumerate(roles):
    role_data = df_clean[df_clean["job_role"] == role].sort_values("year")

    fig.add_trace(go.Scatter(
        x=role_data["year"],
        y=role_data["salary_usd"],
        mode="lines+markers",
        name=role,
        line=dict(color=colors[i % 5],width=3)
    ))

fig.update_layout(
    template="plotly_dark",
    title="Salary Trends",
    xaxis_title="Year",
    yaxis_title="Salary",
    hovermode="x unified"
    
)
fig.update_layout(
    width=900,
    height=400
    #xaxis=dict(showline=True, linewidth=1, linecolor='gray', mirror=True),
    #yaxis=dict(showline=True, linewidth=1, linecolor='gray', mirror=True)
)

country_jobs = df_2026.groupby('country',as_index=False)['job_openings'].sum()
custom_scale = [
    [0.0, "#0b1320"],   # dark navy
    [0.25, "#1f3b73"],  # deep blue
    [0.5, "#4C78A8"],   # blue
    [0.75, "#F58518"],  # orange
    [1.0, "#E45756"]    # red
]
fig2 = px.choropleth(
    country_jobs,
    locations="country",
    locationmode="country names",
    color="job_openings",
    color_continuous_scale=custom_scale,
    title="Number of AI Jobs by Country (2026)"
)
fig2.update_layout(
    template="plotly_dark",
    geo=dict(showcoastlines=True)
    
)
fig2.update_layout(
    geo=dict(
        showframe=True,
        framecolor="gray",
        framewidth=2
    )
)

f1,f2=st.columns(2)
with f1:
    st.plotly_chart(fig,use_container_width=True)
with f2:
    st.plotly_chart(fig2,use_container_width=True)
job_role=df['job_role'].unique()
def update_role():
    st.session_state.selected_role = st.session_state.temp_role   
if "selected_role" not in st.session_state:
    st.session_state.selected_role = df['job_role'].unique()[0]
filtered=df[df['job_role']==st.session_state.selected_role]
cc,cc2=st.columns(2)
co1,co2,co3=st.columns(3)
with co1:
    selected=st.selectbox('Select role: ', 
                          job_role,
                          index=list(job_role).index(st.session_state.selected_role),
                          key='temp_role',
                          on_change=update_role)
st.session_state.selected_role = selected   
col1,col2=st.columns([0.5,0.5])
with col1:
    groubed_openings=filtered.groupby('year',as_index=False)['job_openings'].sum()
    fig4=px.line(
        groubed_openings,
        x='year',
        y='job_openings',
        title=f'jop openings Over Time for {st.session_state.selected_role}',
        markers=True
        )
    st.plotly_chart(fig4,use_container_width=True)
with col2:
    #st.plotly_chart(fig2,use_container_width=True)
    
    groubed=filtered.groupby('year',as_index=False)['layoff_risk'].mean()
    fig3=px.line(
        groubed,
        x='year',
        y='layoff_risk',
        title=f'Layoff Over Time for {st.session_state.selected_role}',
        markers=True)
    st.plotly_chart(fig3)
#col1,col2,col3=st.columns(3)
# with col2:
#     selected=st.selectbox('Select role: ', 
#                           job_role,
#                           index=list(job_role).index(st.session_state.selected_role),
#                           key='temp_role',
#                           on_change=update_role)
# st.session_state.selected_role = selected  
c1,c2=st.columns(2)
with c1:
    work_mode=filtered['work_mode'].value_counts().reset_index()
    work_mode.columns=['Work Mode','Count']
    fig_work=px.pie(
        work_mode,
        names='Work Mode',
        values='Count',
        title=f'Work Mode Distribution for {st.session_state.selected_role}'
    )
    st.plotly_chart(fig_work,use_container_width=True)
groub_country=filtered.groupby('country',as_index=False)['job_openings'].sum().sort_values('job_openings')
with c2:
    fig_country=px.bar(
        groub_country,
        x='job_openings',
        y='country',
        title=f'Hiring countries for {st.session_state.selected_role}',
        orientation='h'
    )
    st.plotly_chart(fig_country,use_container_width=True)
btn=st.button('Show Sample data')
if btn:
    st.dataframe(df.sample(10))
    c1,c2,c3,c4,c5,c6=st.columns(6)
    with c1:
        st.download_button(
    label="Download data",
    data=df.to_csv(index=False),
    file_name="data.csv",
    mime="text/csv"
)
    with c2:
        btn2=st.button('Hide')
        if btn2:
            btn=False


# coding: utf-8

# In[1]:





# In[2]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


# In[3]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# In[4]:


df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})


# In[5]:


df.head()


# In[6]:


fig=px.bar(df,x='Fruit',y='Amount',color='City',barmode='group')


# In[7]:


app.layout=html.Div(children=[
    html.H1(children='First Dash App'),
    
    dcc.Graph(
    id='starting-with-dash-bar-graph',
    figure=fig
    )
])


# In[11]:


# app.run_server(mode='jupyterlab', port = 8090, dev_tools_ui=True, #debug=True,
#               dev_tools_hot_reload =True, threaded=True)


# In[10]:


if __name__=='__name__':
    app.run_server(debug=False)


import pandas as pd
import plotly.graph_objects as go
df = pd.read_csv(r"https://github.com/rasedul/Sankey-Diagram/blob/main/ticket.csv")

# Source value create
df_temp1 = df.groupby(["Pclass","Sex"]) ["Name"].count().reset_index()
df_temp1.columns = ["source","target","value"]

df_temp1["source"] = df_temp1.source.map({1 :"First Class", 2 :"Business Class", 3:"Economy Class"})

# Target value create
df_temp2 = df.groupby(["Sex","Survived"]) ["Name"].count().reset_index()
df_temp2.columns = ["source","target","value"]

df_temp2["target"] = df_temp2.target.map({1 :"Survived", 0 :"Died"})

# Link Source & Target
links = pd.concat([df_temp1, df_temp2], axis=0)

unique_source_target = list(pd.unique(links[["source","target"]].values.ravel("K")))

mapping_dict = {k: v for v, k in enumerate(unique_source_target)}


links["source"] = links["source"].map(mapping_dict)
links["target"] = links["target"].map(mapping_dict)

links_dict =links.to_dict(orient ="list")

# Node Colors
color_for_nodes =['steelblue', 'gold', 'LightSkyBlue', "lightpink", "goldenrod", 
                  'indianred', 'lightgreen']
              
# Link Colours
color_for_links =["lightpink" , "goldenrod", "lightpink", "goldenrod", "lightpink", "goldenrod",
                  'red', 'green', 'red', 'green']
                  
# Sankey Diagram create

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = unique_source_target,
      color = "blue"
    ),
    link = dict(
      source = links_dict["source"],
      target = links_dict["target"],
      value = links_dict["value"]
  ))])
     

fig.update_layout(title_text="Airplane Passenser's Survival Sankey Diagram", font_size=10)
fig.update_traces(node_color = color_for_nodes,
                  link_color = color_for_links)
fig.show()

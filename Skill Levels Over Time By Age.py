import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("logs.csv")

# Extract relevant columns
cols=['skill_level_know','skill_level_priority',"skill_level_refusal","skill_level_me","skill_level_people",
      "event_time_dbl","event_id", "player_id", "avatar_age"]
df=df[cols]

df=df.fillna(method="ffill")

stack_indices = df.index[df["event_id"] == 200]
df = df.iloc[stack_indices]
print(df)

# Retrieve minigame skill levels of each individual player at the last time they entered the Stack
# Replace the time player entered Stack with "i" so event_times for different players are equal and
# the mean can be taken later
def get_skills(i):
      skills_at_time_i = df[df["event_time_dbl"] < i].groupby("player_id").max("event_time_dbl")
      skills_at_time_i = skills_at_time_i.reset_index()
      for j in skills_at_time_i["event_time_dbl"]:
            skills_at_time_i = skills_at_time_i.replace(j, i)
      return skills_at_time_i

# Takes snapshots of minigame skill levels of each player every 500 seconds and concatenates into a
# dataframe
skills_to_add = [get_skills(i) for i in range(100, 45000, 500)]
skills_over_time = pd.concat(skills_to_add, ignore_index=True)
print(skills_over_time)

# Takes the mean of minigame skill levels at each combination of age and time interval
skills_over_time_by_age = skills_over_time.groupby(["avatar_age", "event_time_dbl"]).mean(["skill_level_know",
                                                                       "skill_level_priority",
                                                                       "skill_level_refusal",
                                                                       "skill_level_me",
                                                                       "skill_level_people"])
skills_over_time_by_age = skills_over_time_by_age.reset_index()
print(skills_over_time_by_age)
print(skills_over_time_by_age.iloc[-1])

# Plots minigame skill levels over time, split by age

# palette = sns.color_palette(["#C37963", "#BB9E95", "#9FCDCA", "#5E7D7F"])
# palette = sns.color_palette(["#40B5AF", "#D06A74", "#593C8F", "#64DD58"])

palette = sns.color_palette(["#D589B0", "#493841", "#E568AE", "#33C8CA"])

sns.set_theme()
fig, axes = plt.subplots(3, 2, figsize=(12,8))
sns.lineplot(x="event_time_dbl", y="skill_level_refusal", hue="avatar_age", palette=palette, data=skills_over_time_by_age, ax=axes[0, 0])
axes[0, 0].set_title("Refusal Skill Over Time By Age")
axes[0, 0].set_ylabel("Refusal Skill")
axes[0, 0].set_xlabel("Time (s)")
sns.lineplot(x="event_time_dbl", y="skill_level_priority", hue="avatar_age", palette=palette, data=skills_over_time_by_age, ax=axes[0, 1])
axes[0, 1].set_title("Priority Skill Over Time By Age")
axes[0, 1].set_ylabel("Priority Skill")
axes[0, 1].set_xlabel("Time (s)")
sns.lineplot(x="event_time_dbl", y="skill_level_people", hue="avatar_age", palette=palette, data=skills_over_time_by_age, ax=axes[1, 0])
axes[1, 0].set_title("People Skill Over Time By Age")
axes[1, 0].set_ylabel("People Skill")
axes[1, 0].set_xlabel("Time (s)")
sns.lineplot(x="event_time_dbl", y="skill_level_know", hue="avatar_age", palette=palette, data=skills_over_time_by_age, ax=axes[1, 1])
axes[1, 1].set_title("Know Skill Over Time By Age")
axes[1, 1].set_ylabel("Know Skill")
axes[1, 1].set_xlabel("Time (s)")
sns.lineplot(x="event_time_dbl", y="skill_level_me", hue="avatar_age", palette=palette, data=skills_over_time_by_age, ax=axes[2, 0])
axes[2, 0].set_title("Me Skill Over Time By Age")
axes[2, 0].set_ylabel("Me Skill")
axes[2, 0].set_xlabel("Time (s)")

fig.delaxes(axes[2, 1]) # deletes 6th subplot
fig.suptitle("Skill Levels Over Time By Age")
plt.tight_layout() # avoids overlap of subplot axes
plt.show()
fig.savefig("Skill Levels Over Time By Age.png", dpi=300)

# Refusal Skill graph only
refusal_graph = sns.lineplot(x="event_time_dbl", y="skill_level_refusal", hue="avatar_age", palette=palette, data=skills_over_time_by_age)
refusal_graph.set_title("Refusal Skill Over Time By Age")
refusal_graph.set_ylabel("Refusal Skill")
refusal_graph.set_xlabel("Time (s)")
plt.legend(title="Age", loc="upper left", labels=["11", "12", "13", "14"], title_fontsize=12, fontsize=12)

plt.show()
refusal_graph.figure.savefig("Refusal Skill Over Time By Age.png", dpi=300)
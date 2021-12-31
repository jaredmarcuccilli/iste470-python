import math
from datetime import date

# Jared Marcuccilli
# ISTE-470 Project

# --- Functions ---

def read_input(_fileName):
    print ("Reading data...")
    f = open(_fileName, "r", encoding="utf-8-sig")

    attributes_line = f.readline().strip() # Read line of attributes
    attributes = attributes_line.split(",")

    data = []

    line = f.readline().strip() # Read first line of data

    video_count = 0
    while line:
        line_list = []
        line_split = line.split(",")
        #line_list.append(line_split[0]) # video_id
        line_list.append(line_split[1]) # trending_count
        # line_list.append(line_split[2]) # trending_date
        #line_list.append(line_split[3]) # title
        #line_list.append(line_split[4]) # channel_title
        line_list.append(line_split[5]) # category_id
        # line_list.append(line_split[6]) # publish_time
        #line_list.append(line_split[7]) # tags
        line_list.append(line_split[8]) # views
        line_list.append(line_split[9]) # likes
        line_list.append(line_split[10]) # dislikes
        line_list.append(line_split[11]) # comment_count
        #line_list.append(line_split[12]) # thumbnail_link
        line_list.append(line_split[13]) # comments_disabled
        line_list.append(line_split[14]) # ratings_disabled
        line_list.append(line_split[15]) # video_error_or_removed
        #line_list.append(line_split[16]) # description

        line_list.append(len(line_split[3])) # 17 title length
        if "title_length" not in attributes:
            attributes.append("title_length")

        line_list.append(len(line_split[16])) # 18 description length
        if "description_length" not in attributes:
            attributes.append("description_length")

        publish_year = line_split[6].split("T")[0].split("-")[0] # publish date
        publish_month = line_split[6].split("T")[0].split("-")[1]
        publish_day = line_split[6].split("T")[0].split("-")[2]
        publish_date = date(int(publish_year), int(publish_month), int(publish_day))

        publish_hour = line_split[6].split("T")[1].split(":")[0].lstrip("0") # 19 publish hour
        


        if publish_hour == "":
            publish_hour = "0"
        # line_list.append(publish_hour)

        if int(publish_hour) >= 4 and int(publish_hour) <= 12:
            # publish_time = "Morning"
            line_list.append("Morning")
        elif int(publish_hour) > 12 and int(publish_hour) < 20:
            # publish_time = "Afternoon"
            line_list.append("Afternoon")
        elif int(publish_hour) >= 20 or int(publish_hour) < 4:
            # publish_time = "Night"
            line_list.append("Night")
        #print(line_split[0] + "Publish Hour: " + str(publish_hour))
        if "publish_hour_disc" not in attributes:
            attributes.append("publish_hour_disc")
        
        trending_year = "20" + line_split[2].split(".")[0] # trending date
        trending_day = line_split[2].split(".")[1]
        trending_month = line_split[2].split(".")[2]
        trending_date = date(int(trending_year), int(trending_month), int(trending_day))
        
        delta = trending_date - publish_date

        line_list.append(len(line_split[7].split("|"))) # 20 number of tags
        if "num_of_tags" not in attributes:
            attributes.append("num_of_tags")

        line_list.append(delta.days) # 21 days to trending
        if "days_to_trending" not in attributes:
            attributes.append("days_to_trending")

        if int(line_split[1]) <= 4: # discretize trending_count
            line_list.append("low")
        elif int(line_split[1]) > 4:
            line_list.append("high")
        if "trending_count_disc" not in attributes:
            attributes.append("trending_count_disc")

        if int(delta.days) <= 1: # discretize days_to_trending
            line_list.append("low")
        elif int(delta.days) > 1 and int(delta.days) <= 3:
            line_list.append("medium")
        elif int(delta.days) > 3:
            line_list.append("high")
        if "days_to_trending_disc" not in attributes:
            attributes.append("days_to_trending_disc")

        if int(len(line_split[3])) <= 40: # discretize title_length
            line_list.append("low")
        elif int(len(line_split[3])) > 40 and int(len(line_split[3])) <= 60:
            line_list.append("medium")
        elif int(len(line_split[3])) > 60:
            line_list.append("high")
        if "title_length_disc" not in attributes:
            attributes.append("title_length_disc")

        if int(len(line_split[16])) <= 500: # discretize description_length
            line_list.append("low")
        elif int(len(line_split[16])) > 500 and int(len(line_split[16])) <= 1500:
            line_list.append("medium")
        elif int(len(line_split[16])) > 1500:
            line_list.append("high")
        if "description_length_disc" not in attributes:
            attributes.append("description_length_disc")

        if int(len(line_split[7].split("|"))) <= 12: # discretize num_of_tags
            line_list.append("low")
        elif int(len(line_split[7].split("|"))) > 12 and int(len(line_split[7].split("|"))) <= 28:
            line_list.append("medium")
        elif int(len(line_split[7].split("|"))) > 28:
            line_list.append("high")
        if "num_of_tags_disc" not in attributes:
            attributes.append("num_of_tags_disc")

        

        if delta.days <= 31: # don't add videos if days to trending is > 31
            if "24" in line_split[5] or "10" in line_split[5] or  "26" in line_split[5] or "23" in line_split[5] or "25" in line_split[5]: # only add if category is x 
                data.append(line_list)
                video_count += 1
        
        line = f.readline().strip()
    
    print("Videos: " + str(video_count))
    print("Attributes: " + str(len(attributes)))
    f.close()

    return attributes, data

def write_output(_attributes, _data):
    print ("Writing data...")
    f = open("output.arff", "w")

    f.write("@RELATION videos\n")

    #f.write("@ATTRIBUTE video_id STRING\n")
    f.write("@ATTRIBUTE trending_count NUMERIC\n")
    # f.write("@ATTRIBUTE trending_date STRING\n")
    #f.write("@ATTRIBUTE title STRING\n")
    #f.write("@ATTRIBUTE channel_title STRING\n")
    f.write("@ATTRIBUTE category_id {2,1,10,15,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44}\n")
    # f.write("@ATTRIBUTE publish_time STRING\n")
    #f.write("@ATTRIBUTE tags STRING\n")
    f.write("@ATTRIBUTE views NUMERIC\n")
    f.write("@ATTRIBUTE likes NUMERIC\n")
    f.write("@ATTRIBUTE dislikes NUMERIC\n")
    f.write("@ATTRIBUTE comment_count NUMERIC\n")
    #f.write("@ATTRIBUTE thumbnail_link STRING\n")
    f.write("@ATTRIBUTE comments_disabled {TRUE,FALSE}\n")
    f.write("@ATTRIBUTE ratings_disabled {TRUE,FALSE}\n")
    f.write("@ATTRIBUTE video_error_or_removed {TRUE,FALSE}\n")
    #f.write("@ATTRIBUTE description STRING\n")
    f.write("@ATTRIBUTE title_length NUMERIC\n")
    f.write("@ATTRIBUTE description_length NUMERIC\n")
    f.write("@ATTRIBUTE publish_hour_disc {Morning,Afternoon,Night}\n")
    f.write("@ATTRIBUTE num_of_tags NUMERIC\n")
    f.write("@ATTRIBUTE days_to_trending NUMERIC\n")
    f.write("@ATTRIBUTE trending_count_disc {low,high}\n")
    f.write("@ATTRIBUTE days_to_trending_disc {low,medium,high}\n")
    f.write("@ATTRIBUTE title_length_disc {low,medium,high}\n")
    f.write("@ATTRIBUTE description_length_disc {low,medium,high}\n")
    f.write("@ATTRIBUTE num_of_tags_disc {low,medium,high}\n")

    f.write("@DATA\n")

    for line in data:
        for x in range(0, 18):
            f.write(str(line[x]) + ",")
        f.write(str(line[18]) + "\n")

    f.close()

# --- Main Program ---

attributes, data = read_input("input.csv")
write_output(attributes, data)

#print(attributes)
#print(data)

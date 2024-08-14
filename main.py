import math
from random import randrange
import pandas as pd
import pyautogui
import cv2
import numpy as np
import time
import mss.tools
import pytesseract
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
    
def click_at(x, y):
    pyautogui.click(x, y)

def click_image(image_path, timeout=10):
    try:
        # Wait for the image to appear on the screen for a specified timeout
        start_time = time.time()
        while time.time() - start_time < timeout:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location is not None:
                # Click the center of the found image
                location_x = location[0]/2
                location_y = location[1]/2
                click_at(location_x, location_y)
                print(f"Clicked on {image_path}")
                return True
            time.sleep(1)  # Wait for 1 second before checking again

        print(f"Image {image_path} not found within the timeout.")
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False
    
def locate_image(image_path, timeout=10):
    try:
        # Wait for the image to appear on the screen for a specified timeout
        start_time = time.time()
        while time.time() - start_time < timeout:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location is not None:
                # Click the center of the found image
                location_x = location[0]/2
                location_y = location[1]/2
                return location_x, location_y
            time.sleep(1)  # Wait for 1 second before checking again

        print(f"Image {image_path} not found within the timeout.")
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False
    
def plane_needs_loading(row_number, cargo_height):
    with mss.mss() as sct: 
        section = {"top": 137 + (row_number * cargo_height), "left": 1012, "width": 110, "height": 37}
        output = "plane_status.png".format(**section)
        sct_img = sct.grab(section)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

        image = cv2.imread('plane_status.png')
        image = cv2.resize(image, None, fx=1, fy=1)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        plane_status = pytesseract.image_to_string(image).strip()
        if similar(plane_status, 'BOARDING') >= 0.6 or similar(plane_status, 'LANDED') >= 0.6 or similar(plane_status, 'IDLE') >= 0.6:
            return True
        else:
            return False
    
def locate_boarding():
    try:
        boarding_planes = list(pyautogui.locateAllOnScreen('boarding.png', confidence = 0.8))
        fixed_boarding_planes = []
        fixed_boarding_planes.append(boarding_planes[0])
        for i in range(1, len(boarding_planes)):
            if boarding_planes[i].top > fixed_boarding_planes[len(fixed_boarding_planes)-1].top + 50:
                fixed_boarding_planes.append(boarding_planes[i])
        if boarding_planes is not None:
            return fixed_boarding_planes
    except Exception as e:
        print(f"Error: {e}")
    return False

def select_cargo(first_cargo_top):
    pass   
    
def find_target_cargo(cargo_description_start_x, cargo_description_start_y, cargo_description_width, cargo_height,
                      destination):
    with mss.mss() as sct:
        cargo_x = cargo_description_start_x
        cargo_y = cargo_description_start_y
        for i in range(0,11):
            monitor = {"top": cargo_y, "left": cargo_x, "width": cargo_description_width, "height": cargo_description_height}
            output = "cargo_" + str(i) + ".png".format(**monitor)

            # Grab the data
            sct_img = sct.grab(monitor)
            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            image = cv2.imread('cargo_'+str(i)+'.png')
            image = cv2.resize(image, None, fx=0.8, fy=0.8)
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            text = pytesseract.image_to_string(image) 
            if len(text.split('-')) > 1:
                city = text.split('-')[0].strip()
            else:
                city = text.split('=')[0].strip()
            
            if similar(city,destination) >= 0.6:
                return i
            
            cargo_y = cargo_y + cargo_height
    return -1
            
def checkForBonus():
    try: 
        location = pyautogui.locateCenterOnScreen("bonus.png", confidence=0.8)
        if location is not None:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    
def plane_full():
    try: 
        location = pyautogui.locateCenterOnScreen("bonus.png", confidence=0.8)
        if location is not None:
            return True
        else:
            return False
    except Exception as e:
        try:
            time.sleep(0.5)
            full_plane_indicator = pyautogui.locateOnScreen('full_plane.png', confidence=0.95)
            if full_plane_indicator is not None:
                return True
        except Exception as e:
            print(f"Error: {e}")
        return False
    
def fly(plane_start_x, plane_start_y, coordinates_file, all_coordinates, source, event_destination, event, event_coordinates, 
        source_coordinates, cargo_height, cargo_description_start_x, cargo_description_start_y, cargo_description_height, 
        cargo_description_width, plane_range):
        location = pyautogui.locateCenterOnScreen("fly.png", confidence=0.8)
        if location is not None:
                    # MAY BE USED IN THE FUTURE 
                    # with mss.mss() as sct: 
                    #     section = {"top": 455, "left": 544, "width": 53, "height": 18}
                    #     output = "plane_name.png".format(**section)
                    #     sct_img = sct.grab(section)
                    #     mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

                    # image = cv2.imread('plane_name.png')
                    # image = cv2.resize(image, None, fx=2, fy=2)
                    # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                    # plane_name = pytesseract.image_to_string(image).strip()

                    # NEED REPLACEMENT FOR BELOW COMMENTED CODE?
                    # if coordinates is not None:
                    #     x,y = coordinates
                    # else:
                    #     x,y = find_plane_coordinates(plane_start_x, plane_start_y)
                    #     new_row = {"name": plane_name, "x": x, "y": y}
                    #     new_row_df = pd.DataFrame([new_row])
                    #     all_coordinates = pd.concat([all_coordinates, new_row_df], ignore_index=True)

                    origin_coordinates = source_coordinates

                    #below 2 lines are likely redundant (with removal/revamp of event cdode)
                    current_point = origin_coordinates
                    closest_point_coordinates = 0,0

                    if event is True and similar(source, event_destination) < 0.6:
                        dest, dest_coordinates = event_destination, event_coordinates
                    else:
                        dest, dest_coordinates = identify_destination(cargo_description_start_y, cargo_height, cargo_description_start_x, 
                                                                      cargo_description_height, cargo_description_width, all_coordinates)
                    
                    location_x = location[0]/2
                    location_y = location[1]/2
                    click_at(location_x, location_y)
                    print(f"Clicked on fly")
                    time.sleep(0.5)

                    path_coordinates = find_path(all_coordinates, source, dest, source_coordinates, plane_range)
                    for p in range(1, len(path_coordinates)):
                        current_point = path_coordinates[p-1]
                        print('current point: ', current_point)
                        target_point = path_coordinates[p]
                        print('target point: ', target_point)
                        distance_to_travel = math.dist(current_point, target_point)
                        print('distance to travel: ', distance_to_travel)
                        while distance_to_travel > 300:
                            print('entered while loop')
                            # Calculate the vector from source to target
                            direction_vector = target_point - current_point
                            # Normalize the direction vector to get a unit vector
                            unit_vector = direction_vector / np.linalg.norm(direction_vector)
                            # Calculate the new point
                            new_point = current_point + 300 * unit_vector
                            print('new_point: ', new_point)
                            target_screen_x = plane_start_x + (new_point[0] - current_point[0])
                            target_screen_y = plane_start_y + (new_point[1] - current_point[1])
                            print('target_screen_x: ', target_screen_x)
                            print('target_screen_y: ', target_screen_y)
                            pyautogui.moveTo(target_screen_x, target_screen_y, duration=1, tween=pyautogui.easeInOutQuint)
                            pyautogui.dragTo(plane_start_x, plane_start_y, duration=1, tween=pyautogui.easeInOutQuint, button="left")
                            distance_to_travel = distance_to_travel - 300  
                            print('new distance to travel: ', distance_to_travel)
                            current_point = new_point
                        target_screen_x = plane_start_x + (target_point[0] - current_point[0])
                        print('exited while loop')
                        print('target_screen_x: ', target_screen_x)
                        target_screen_y = plane_start_y + (target_point[1] - current_point[1])
                        print('target_screen_y: ', target_screen_y)
                        pyautogui.leftClick(target_screen_x, target_screen_y, duration=1, tween=pyautogui.easeInOutQuint)
                        pyautogui.dragTo(plane_start_x, plane_start_y, duration=1, tween=pyautogui.easeInOutQuint, button="left")
                    
                    click_image('fly2.png')
                    all_coordinates.to_csv(coordinates_file, index=False)
                    print(f"\nDataFrame saved to {coordinates_file}")

def find_path(all_coordinates, source, dest, source_coordinates, plane_range):
    print('source as printed ( i think )', source)
    filtered_rows = all_coordinates[all_coordinates['name'].apply(lambda x: similar(x, dest)) >= 0.5]
    filtered_rows['similarity'] = filtered_rows['name'].apply(lambda x: similar(x, dest))
    sorted_rows = filtered_rows.sort_values(by='similarity', ascending=False)
    destination = sorted_rows[['name']].values[0][0]
    print('destination: ', destination)
    filtered_rows = all_coordinates[all_coordinates['name'].apply(lambda x: similar(x, source)) >= 0.5]
    filtered_rows['similarity'] = filtered_rows['name'].apply(lambda x: similar(x, source))
    sorted_rows = filtered_rows.sort_values(by='similarity', ascending=False)
    source = sorted_rows[['name']].values[0][0]
    print('source: ', source)
    print("sorted_rows[['name']].values[0][0]: ", sorted_rows[['name']].values[0][0])
    source_x, source_y = source_coordinates[0], source_coordinates[1]
    djikstra = all_coordinates.copy()
    djikstra['distance_from_source'] = np.sqrt((djikstra['x']-source_x)**2 + (djikstra['y']-source_y)**2)
    djikstra = djikstra[djikstra.distance_from_source < 
                        djikstra.loc[djikstra['name']==destination, 'distance_from_source'].values[0]*1.5].reset_index(drop=True)
    djikstra['shortest_path'] = None
    djikstra['shortest_distance'] = None
    djikstra['visited'] = False
    print(djikstra)
    source_index = djikstra.index[djikstra['name'] == source].values[0]
    destination_index = djikstra.index[djikstra['name'] == destination].values[0]
    neighbors_dataframes = []
    neighbors_dataframes_base = djikstra.copy()
    neighbors_dataframes_base.drop('distance_from_source', axis=1, inplace=True)
    neighbors_dataframes_base.drop('shortest_path', axis=1, inplace=True)
    neighbors_dataframes_base.drop('shortest_distance', axis=1, inplace=True)

    for index, airport in djikstra.iterrows():
        neighbors = neighbors_dataframes_base.copy()
        airport_x = neighbors.loc[index, 'x']
        airport_y = neighbors.loc[index, 'y']
        neighbors['distance_from_'+airport['name']] = np.sqrt((neighbors['x']-airport_x)**2 + (neighbors['y']-airport_y)**2)
        neighbors = neighbors.loc[(neighbors['distance_from_'+airport['name']] <= plane_range) & 
                                    (neighbors['distance_from_'+airport['name']] > 0)]
        neighbors_dataframes.append(neighbors)
        
        djikstra.at[source_index, 'shortest_path'] = [source_index]
        djikstra.at[source_index, 'shortest_distance'] = 0
        djikstra.at[source_index, 'visited'] = True

    current_airport_idx = source_index
    visitable_neighbors = pd.DataFrame()

    while not djikstra['visited'].all():
        min_distance = None # neighbor with shortest distance to source
        min_path = [] # the path associated
        winning_neighbor_idx = None
        # iterate through neighbors' dataframes containing their neighbors
        visitable_neighbors = pd.concat([visitable_neighbors, neighbors_dataframes[current_airport_idx]])
        for neighbor_idx, neighbor in visitable_neighbors.iterrows():
            # ignore neighbors that have already been visited
            if not djikstra.loc[neighbor_idx, 'visited']:
                # retrieve distance from the current airport, which is the last visited airport, to this neighbor
                # retrieve the candidate shortest distance from the source to this neighbor
                # calculate distance from source through current airport to this neighbor
                distance_to_this_neighbor = neighbor.iloc[3]
                shortest_distance_for_this_neighbor = djikstra.loc[neighbor_idx, 'shortest_distance']
                total_dist_from_this_to_neighbor = None
                if distance_to_this_neighbor <= plane_range:
                    total_dist_from_this_to_neighbor = djikstra.loc[current_airport_idx, 'shortest_distance'] + distance_to_this_neighbor
                    # if there has not been a previous candidate for shortest path from source to this neighbor,
                    # or if it exists, but the path through the current airport is shorter than that
                    # replace the shortest_distance and shortest_path for this neighbor in the djikstra dataframe with the 
                    # distance and path through this airport 
                    if (djikstra.loc[neighbor_idx, 'shortest_path'] == None or 
                        total_dist_from_this_to_neighbor < shortest_distance_for_this_neighbor):
                        djikstra.at[neighbor_idx, 'shortest_path'] = \
                        djikstra.loc[current_airport_idx, 'shortest_path'] + [neighbor_idx]
                        djikstra.at[neighbor_idx, 'shortest_distance'] = total_dist_from_this_to_neighbor
                # next update the minimum distance out of distances from source to all unvisited adjacent airports
                if (min_distance == None or total_dist_from_this_to_neighbor and total_dist_from_this_to_neighbor < min_distance):
                    min_distance = total_dist_from_this_to_neighbor
                    winning_neighbor_idx = neighbor_idx
                elif (shortest_distance_for_this_neighbor is not None and shortest_distance_for_this_neighbor < min_distance):
                    min_distance = shortest_distance_for_this_neighbor
                    winning_neighbor_idx = neighbor_idx
                    
        djikstra.at[winning_neighbor_idx, 'visited'] = True
        if winning_neighbor_idx == destination_index:
            path_indices = djikstra.loc[djikstra['name'] == destination, 'shortest_path'].values[0]
            path_coordinates = np.array(djikstra.loc[path_indices, ['x', 'y']].values.tolist())
            print(djikstra)
            print(path_coordinates)
            print(source)
            print(destination)
            return path_coordinates
        if (len(neighbors_dataframes[winning_neighbor_idx]) > 1):
            current_airport_idx = winning_neighbor_idx



def find_plane_coordinates(plane_start_x, plane_start_y):
        time.sleep(0.5)

        with mss.mss() as sct:
            section = {"top": 476, "left": 558, "width": 30, "height": 25}
            output = "start_picture.png".format(**section)
            sct_img = sct.grab(section)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

        for _ in range(0,15):
            pyautogui.moveTo(plane_start_x - 300, plane_start_y, duration=1, tween=pyautogui.easeInOutQuint)
            pyautogui.dragTo(plane_start_x, plane_start_y, duration=1, tween=pyautogui.easeInOutQuint, button="left")

        city_x_coordinate = 0
        city_y_coordinate = 0
        current_x_coordinate = plane_start_x
        current_y_coordinate = plane_start_y

        while True:
            time.sleep(0.5)
            try: 
                found_start = pyautogui.locateCenterOnScreen('start_picture.png', confidence = 0.9)
                if found_start is not None:
                    found_start_x = found_start[0]/2
                    found_start_y = found_start[1]/2
                    if (found_start_x - plane_start_x <= 300):
                        if found_start_x < plane_start_x:
                            city_x_coordinate = current_x_coordinate + found_start_x
                            print('and city_x coordinate has been set to.. (case of found start less than plane start)', city_x_coordinate)
                        else:
                            city_x_coordinate = current_x_coordinate + (found_start_x - plane_start_x)
                            print('and city_x coordinate has been set to.. ', city_x_coordinate)
                        pyautogui.moveTo(found_start_x, plane_start_y, duration=1, tween=pyautogui.easeInOutQuint)
                        pyautogui.dragTo(plane_start_x, plane_start_y, duration=1, tween=pyautogui.easeInOutQuint, button="left")  
                        break  
                    else:
                        current_x_coordinate = current_x_coordinate + 300
                        print('a bit out of reach, adding 300: ', current_x_coordinate)
            except Exception as e:
                print(f"Error: {e}")
                current_x_coordinate = current_x_coordinate + 300
                print("it's not on the screen, adding 300: ", current_x_coordinate)
            pyautogui.moveTo(plane_start_x + 300, plane_start_y, duration=1, tween=pyautogui.easeInOutQuint)
            pyautogui.dragTo(plane_start_x, plane_start_y, duration=1, tween=pyautogui.easeInOutQuint, button="left")

        for _ in range(0,10):
            pyautogui.moveTo(plane_start_x, plane_start_y-300, duration=1, tween=pyautogui.easeInOutQuint)
            pyautogui.dragTo(plane_start_x, plane_start_y, duration=1, tween=pyautogui.easeInOutQuint, button="left")

        while True:
            time.sleep(0.5)
            try: 
                found_start = pyautogui.locateCenterOnScreen('start_picture.png', confidence = 0.9)
                if found_start is not None:
                    found_start_x = found_start[0]/2
                    found_start_y = found_start[1]/2
                    if (found_start_y - plane_start_y <= 300):
                        if found_start_y < plane_start_y:
                            city_y_coordinate = current_y_coordinate + found_start_y
                        else:
                            city_y_coordinate = current_y_coordinate + (found_start_y - plane_start_y)
                        pyautogui.moveTo(plane_start_x, found_start_y, duration=1, tween=pyautogui.easeInOutQuint)
                        pyautogui.dragTo(plane_start_x, plane_start_y, duration=1, tween=pyautogui.easeInOutQuint, button="left")  
                        break  
                    else:
                        current_y_coordinate = current_y_coordinate + 300
            except Exception as e:
                print(f"Error: {e}")
                current_y_coordinate = current_y_coordinate + 300
            pyautogui.moveTo(plane_start_x, plane_start_y+300, duration=1, tween=pyautogui.easeInOutQuint)
            pyautogui.dragTo(plane_start_x, plane_start_y, duration=1, tween=pyautogui.easeInOutQuint, button="left")
        
        return city_x_coordinate, city_y_coordinate
                    
def get_coordinates(dataframe, point_name):
    try:
        # Locate the row with the specified 'name' and get 'x' and 'y' values
        x, y = dataframe.loc[dataframe['name'] == point_name, ['x', 'y']].values[0]
        return x, y
    except IndexError:
        # Handle the case where the specified 'name' is not found
        print(f"Point with name '{point_name}' not found.")
        return None

def hold_on_board():
    loading_done = False
    try:
        time.sleep(0.5)
        onboard = pyautogui.locateCenterOnScreen('onboard.png', confidence=0.9)
        if onboard is not None:
            onboard_x = onboard[0]/2
            onboard_y = onboard[1]/2
            pyautogui.moveTo(onboard_x, onboard_y)
            pyautogui.dragTo(onboard_x, onboard_y, tween=pyautogui.easeInOutQuint, button='left', 
                                    duration=1)
            pyautogui.moveTo(onboard_x, onboard_y)
            pyautogui.dragTo(onboard_x, onboard_y, tween=pyautogui.easeInOutQuint, button='left', 
                                    duration=1)
            loading_done = True
            time.sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")
        print('i am regretfully here')
    return loading_done

def get_center_coords(point):
    # gets center coords given left, top, width, height
    x = point[0]/2 + point[2]/4
    y = point[1]/2 + point[3]/4
    return x, y

def get_aiport_coordinates(choice_center_y, airport_name_start_x, airport_name_width, cargo_description_height, all_coordinates):
    time.sleep(0.5)
    with mss.mss() as sct:
        monitor = {"top": (choice_center_y - (cargo_description_height/2)), "left": airport_name_start_x, "width": airport_name_width, 
                   "height": cargo_description_height}
        output = "airport.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)
        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        image = cv2.imread('airport.png')
        image = cv2.resize(image, None, fx=0.8, fy=0.8)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        city = pytesseract.image_to_string(image).strip()
        filtered_rows = all_coordinates[all_coordinates['name'].apply(lambda x: similar(x, city)) >= 0.5]
        filtered_rows['similarity'] = filtered_rows['name'].apply(lambda x: similar(x, city))
        sorted_rows = filtered_rows.sort_values(by='similarity', ascending=False)
        x = sorted_rows[['x']].values[0]
        y = sorted_rows[['y']].values[0]
        coordinates = x, y
        return city, coordinates

def identify_destination(cargo_description_start_y, cargo_height, cargo_description_start_x, cargo_description_height, cargo_description_width, all_coordinates):
    for k in range(0,12):
        time.sleep(1)
        try:
            onboard = pyautogui.locateOnScreen('onboard.png', confidence=0.9)
            if onboard is not False:
                with mss.mss() as sct:
                    monitor = {"top": cargo_description_start_y + cargo_height * round((onboard[1]/2-cargo_description_start_y)/cargo_height), "left": cargo_description_start_x, "width": cargo_description_width, "height": cargo_description_height}
                    output = "cargo.png".format(**monitor)
                    sct_img = sct.grab(monitor)
                    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
                    image = cv2.imread('cargo.png')
                    image = cv2.resize(image, None, fx=0.8, fy=0.8)
                    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                    text = pytesseract.image_to_string(image)
                    if len(text.split('-')) > 1:
                        city = text.split('-')[0].strip()
                    else:
                        city = text.split('=')[0].strip()
                    filtered_rows = all_coordinates[all_coordinates['name'].apply(lambda x: similar(x, city)) >= 0.6]
                    filtered_rows['similarity'] = filtered_rows['name'].apply(lambda x: similar(x, city))
                    sorted_rows = filtered_rows.sort_values(by='similarity', ascending=False)
                    x = sorted_rows[['x']].values[0]
                    y = sorted_rows[['y']].values[0]
                    coordinates = x, y
                    return city, coordinates
        except Exception as e:
            print('Error: ', e)
            pyautogui.moveTo(window_middle_x, fifth_cargo_y)
            pyautogui.dragTo(window_middle_x, (fifth_cargo_y-4*cargo_height-4), tween=pyautogui.easeInOutQuint, button='left', 
                            duration=1)
            time.sleep(0.5)

# def select_loads():
    

if __name__ == "__main__": 
    source = None
    event_destination = 'HONG KONG'
    event = True

    pyautogui.keyDown('command')
    pyautogui.press('space')
    pyautogui.keyUp('command')
    pyautogui.write('pocket pl')
    pyautogui.press('enter')
    time.sleep(1.5)
    title_bar = pyautogui.locateOnScreen('title_bar.png', confidence=0.7)
    x_offset = title_bar.left/2
    window_middle_x = x_offset + title_bar.width/4
    window_width = title_bar.width/2
    window_height = 885
    window_middle_y = title_bar.top/2 + 921/2
    window_top = title_bar.top/2
    map_height = 728
    plane_start_x = x_offset + 574
    plane_start_y = 493
    plane_range = 500 # should really be 492 but is 500 due to inaccuracies in airport coordinates

    first_button = load_button = (x_offset + 35, 857)
    second_button = passengers_button = (x_offset + 103, 857)
    third_button = cargo_button = (x_offset  + 172, 857)

    cargo_height = 65.2
    first_cargo_top = 119
    first_cargo_center_y = first_cargo_top + cargo_height/2
    cargo_description_start_x = x_offset + 34
    cargo_description_start_y = 137
    cargo_description_width = 363
    cargo_description_height = 28
    fifth_cargo_y = 413.16
    first_load_button_left = x_offset + 1065
    first_load_button_top = 142
    load_button_width = 53
    load_button_height = 20
    load_button_middle_x = x_offset + 1089
    first_load_button_middle_y = 142 + load_button_height/2

    airport_name_start_x = 349
    airport_name_width = 200

    coordinates_file = 'coordinates.csv'
    event_coordinates = 0
    source_coordinates = 0

    try:
        # Attempt to read the CSV file
        all_coordinates = pd.read_csv(coordinates_file)
        # dest_coordinates = 
        # Display the DataFrame read from the CSV file
        print("DataFrame read from CSV:")
        print(all_coordinates)
        if event:
            temp_x = all_coordinates.loc[all_coordinates['name']==event_destination, 'x'].iloc[0]
            temp_y = all_coordinates.loc[all_coordinates['name']==event_destination, 'y'].iloc[0]
            event_coordinates = temp_x, temp_y

    except FileNotFoundError:
        all_coordinates = pd.DataFrame(columns=['name', 'x', 'y'])

    boarding_planes = False
    boarding_iterator = 0
    
    while True:
        q = 0
        limit = 11
        while q < limit:
            click_image('planes.png')
            time.sleep(0.5)
            if plane_needs_loading(q, cargo_height):
                source, source_coordinates = get_aiport_coordinates(155.5 + q * cargo_height, airport_name_start_x, airport_name_width, 
                                                                    cargo_description_height, all_coordinates)
                click_at(1067, 155.5 + q * cargo_height)
                time.sleep(0.2)
                click_at(load_button[0], load_button[1])
                loading_done = False
                cargo_number = -1
                
                if event == True:
                    for k in range(0,5):
                        time.sleep(0.5)
                        cargo_number = find_target_cargo(cargo_description_start_x, cargo_description_start_y, cargo_description_width, 
                                                            cargo_height, event_destination)
                        if cargo_number > -1:
                            break
                        else:
                            pyautogui.moveTo(window_middle_x, fifth_cargo_y)
                            pyautogui.dragTo(window_middle_x, (fifth_cargo_y-4*cargo_height-4), tween=pyautogui.easeInOutQuint, 
                                                button='left', duration=1)
                    loading_done = hold_on_board()
                    if loading_done is False and cargo_number > -1:
                        first_target_found_y = first_cargo_center_y + (cargo_height * cargo_number)
                        pyautogui.moveTo(window_middle_x, first_target_found_y)
                        pyautogui.dragTo(window_middle_x, first_target_found_y, tween=pyautogui.easeInOutQuint, button='left', 
                                        duration=1)
                        loading_done = True
                        time.sleep(0.5)
                else:
                    loading_done = hold_on_board()
                    if loading_done is False:
                        pyautogui.moveTo(window_middle_x, first_cargo_center_y)
                        pyautogui.dragTo(window_middle_x, first_cargo_center_y, tween=pyautogui.easeInOutQuint, button='left', 
                                        duration=1)
                        
                if plane_full():
                    q = q - 1
                    fly(plane_start_x, plane_start_y, coordinates_file, all_coordinates, source, event_destination, event, 
                        event_coordinates, source_coordinates, cargo_height, cargo_description_start_x, cargo_description_start_y, 
                        cargo_description_height, cargo_description_width, plane_range)
            else:
                click_image('continue.png')
                break
            q = q + 1

## previous while true contents
                
# click_image('planes.png')
#         time.sleep(0.2)
#         coords = locate_image('landed.png')
#         if coords is not False:
#             source, source_coordinates = get_aiport_coordinates(coords[1], airport_name_start_x, airport_name_width, cargo_description_height, all_coordinates)
#             click_at(coords[0], coords[1])
#         elif coords is False:
#             coords = locate_image('idle.png')
#             if coords is not False:
#                 source, source_coordinates = get_aiport_coordinates(coords[1], airport_name_start_x, airport_name_width, cargo_description_height, all_coordinates)
#                 click_at(coords[0], coords[1])
#             elif coords is False:
#                 new_boarding_planes = locate_boarding()
#                 if new_boarding_planes is not False:
#                     if boarding_planes is not False:
#                         if new_boarding_planes == boarding_planes:
#                             if boarding_iterator < len(boarding_planes):
#                                 x, y = get_center_coords(boarding_planes[boarding_iterator])
#                                 source, source_coordinates = get_aiport_coordinates(y, airport_name_start_x, airport_name_width, cargo_description_height, 
#                                 all_coordinates)
#                                 click_at(x, y)
#                                 boarding_iterator += 1
#                                 print("boarding iterator: ", boarding_iterator)
#                                 print("len boarding planes: ", len(boarding_planes))
#                                 print('boarding_planes: ', boarding_planes)
#                             else:
#                                 boarding_planes = False
#                                 time.sleep(30)
#                                 continue
#                         else:
#                             boarding_planes = new_boarding_planes
#                             x, y = get_center_coords(boarding_planes[0])
#                             source, source_coordinates = get_aiport_coordinates(y, airport_name_start_x, airport_name_width, cargo_description_height, 
#                                                                         all_coordinates)
#                             click_at(x, y)
#                             boarding_iterator = 1
#                     else:
#                         boarding_planes = new_boarding_planes
#                         x, y = get_center_coords(boarding_planes[0])
#                         source, source_coordinates = get_aiport_coordinates(y, airport_name_start_x, airport_name_width, cargo_description_height, 
#                                                                     all_coordinates)
#                         click_at(x, y)
#                         boarding_iterator = 1
#                 elif click_image('continue.png') is True:
#                     continue
#                 else:
#                     boarding_planes = False
#                     time.sleep(30)
#                     continue 
                        
#         time.sleep(0.2)
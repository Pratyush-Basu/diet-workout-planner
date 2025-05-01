from flask import Flask,render_template,request
import google.generativeai as genai
import os
import markdown
from dotenv import load_dotenv

app= Flask(__name__)

#api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key="GEMINI_API_KEY")  # Replace with your Gemini API key
model = genai.GenerativeModel('gemini-1.5-pro')  # Use Gemini 1.5 Pro

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/recommendation", methods=['POST'])
def recommendation():
    if request.method=='POST':
        #collect form data
        name = request.form['full_name']
        age = request.form['age']
        gender = request.form['gender']
        country=request.form.get('country')
        height = request.form['height']
        weight = request.form['weight']
        fitness_goal = request.form['fitness_goal']
        target_weight = request.form['target_weight']
        diet_type = request.form['diet_type']
        allergies = request.form['allergies']
        meals_per_day = request.form['meals_per_day']
        workout_level = request.form['workout_level']
        workout_types = request.form.getlist('workout_types')  # still use getlist for checkboxes
        workout_days = request.form['workout_days']
        activity_level = request.form['activity_level']
        wake_up = request.form['wake_up']
        bed_time = request.form['bed_time']
        notes = request.form['notes']
        
        # Combine data into a summary or use it for further processing
        prompt = f"""
<|system|>
You are an expert fitness and nutrition coach. Your task is to create a detailed, personalized plan based on user inputs, including diet (breakfast, lunch, dinner, snacks), workout routines, and lifestyle adjustments. Your response must be structured, motivational, and tailored to the individual’s health goals, preferences, allergies, and routine.

<|user|>
Hey {name}, (please make sure the name take from form data)

I'm looking for a personalized health plan to reach my goal. Here are my details:

🔹 **Basic Info**  
- Age: {age}  
- Gender: {gender}
- Country: {country}  
- Height: {height} cm  
- Weight: {weight} kg  
- Target Weight: {target_weight}  
- Fitness Goal: {fitness_goal}  
- Activity Level: {activity_level}

🔹 **Diet Details**  
- Diet Type: {diet_type}   
- Allergies: {allergies}  
- Meals per Day: {meals_per_day}

🔹 **Workout Preferences**  
- Workout Level: {workout_level}  
- Preferred Types: {', '.join(workout_types)}  
- Days per Week: {workout_days}

🔹 **Lifestyle**  
- Wake Up Time: {wake_up}  
- Bed Time: {bed_time}  
- Other Notes: {notes}

Please give me:

1. A **motivational greeting** (use my name)
2. A complete **meal plan** (Breakfast, Lunch, Snacks, Dinner)
3. A **personalized weekly workout routine**, including:
   - Workout split for each day (e.g., Mon: Cardio, Tue: Upper body)
   - Specific exercises (e.g., 3 sets of push-ups, planks)
   - Duration in minutes
   - Suitable for my workout level: {workout_level}
   - Focused on my fitness goal: {fitness_goal}
4. Tips for staying consistent and making lifestyle adjustments if needed.
5. (Optional) Recommend video links or online resources if available.


Be clear and structured. Use bullet points or headings for readability.


Thanks!

"""

            # Get response from DeepSeek model
        response = model.generate_content(prompt)
        plan = response.text
        plan_html= markdown.markdown(plan)
        #print(plan)

        return render_template("result.html", plan=plan_html)
if __name__=="__main__":
    app.run(debug=True)


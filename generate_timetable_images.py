from PIL import Image, ImageDraw, ImageFont
import os

# Create directory if it doesn't exist
output_dir = r"c:\Users\LENOVO\Frs\flutter_attendance\assets\images"
os.makedirs(output_dir, exist_ok=True)

# Define timetable data
timetables = {
    "1st": [
        ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        ["9:00-10:00", "Math", "Physics", "Chemistry", "Biology", "English"],
        ["10:00-11:00", "Physics", "Math", "English", "Chemistry", "Physics"],
        ["11:00-12:00", "Chemistry", "English", "Math", "Physics", "Chemistry"],
        ["12:00-1:00", "Lunch Break", "Lunch Break", "Lunch Break", "Lunch Break", "Lunch Break"],
        ["1:00-2:00", "English", "Chemistry", "Physics", "Math", "Biology"],
        ["2:00-3:00", "Lab", "Lab", "Lab", "Lab", "Lab"]
    ],
    "2nd": [
        ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        ["9:00-10:00", "Data Structures", "Algorithms", "Database", "Networking", "Operating Systems"],
        ["10:00-11:00", "Algorithms", "Data Structures", "Networking", "Database", "Algorithms"],
        ["11:00-12:00", "Database", "Networking", "Data Structures", "Algorithms", "Database"],
        ["12:00-1:00", "Lunch Break", "Lunch Break", "Lunch Break", "Lunch Break", "Lunch Break"],
        ["1:00-2:00", "Networking", "Database", "Algorithms", "Data Structures", "Electives"],
        ["2:00-3:00", "Lab", "Lab", "Lab", "Lab", "Project Work"]
    ],
    "3rd": [
        ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        ["9:00-10:00", "Machine Learning", "Computer Vision", "NLP", "Big Data", "Cybersecurity"],
        ["10:00-11:00", "Computer Vision", "Machine Learning", "Big Data", "NLP", "Computer Vision"],
        ["11:00-12:00", "NLP", "Big Data", "Machine Learning", "Machine Learning", "NLP"],
        ["12:00-1:00", "Lunch Break", "Lunch Break", "Lunch Break", "Lunch Break", "Lunch Break"],
        ["1:00-2:00", "Big Data", "NLP", "Computer Vision", "Cybersecurity", "Electives"],
        ["2:00-3:00", "Lab", "Lab", "Lab", "Lab", "Research"]
    ],
    "4th": [
        ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        ["9:00-10:00", "Project", "Internship Prep", "Thesis", "Seminar", "Industry Visit"],
        ["10:00-11:00", "Internship Prep", "Project", "Seminar", "Thesis", "Internship Prep"],
        ["11:00-12:00", "Thesis", "Seminar", "Project", "Project", "Thesis"],
        ["12:00-1:00", "Lunch Break", "Lunch Break", "Lunch Break", "Lunch Break", "Lunch Break"],
        ["1:00-2:00", "Seminar", "Thesis", "Internship Prep", "Internship Prep", "Electives"],
        ["2:00-3:00", "Lab", "Lab", "Lab", "Lab", "Viva"]
    ]
}

def create_timetable_image(data, filename):
    # Image dimensions
    width = 800
    height = 600
    
    # Create image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a better font, fallback to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 16)
        header_font = ImageFont.truetype("arialbd.ttf", 18)
    except:
        font = ImageFont.load_default()
        header_font = ImageFont.load_default()
    
    # Calculate cell dimensions
    rows = len(data)
    cols = len(data[0])
    cell_width = width // cols
    cell_height = height // rows
    
    # Draw grid and content
    for i in range(rows):
        for j in range(cols):
            # Calculate position
            x1 = j * cell_width
            y1 = i * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            
            # Draw cell border
            draw.rectangle([x1, y1, x2, y2], outline='black')
            
            # Draw text
            text = data[i][j]
            # Center text in cell
            try:
                text_width = draw.textlength(text, font=font if i > 0 else header_font)
            except:
                text_width = len(text) * 10  # Approximate width
            
            text_height = 20  # Approximate height
            text_x = x1 + (cell_width - text_width) // 2
            text_y = y1 + (cell_height - text_height) // 2
            
            # Use different font for header
            if i == 0:
                draw.text((text_x, text_y), text, fill='black', font=header_font)
            else:
                draw.text((text_x, text_y), text, fill='black', font=font)
    
    # Save image
    img.save(filename)
    print(f"Created {filename}")

# Generate timetable images
for year, data in timetables.items():
    filename = os.path.join(output_dir, f"{year}_timetable.png")
    create_timetable_image(data, filename)

print("All timetable images generated successfully!")
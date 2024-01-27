import tkinter as tk
from tkinter import StringVar, filedialog,messagebox
from PIL import ImageTk, Image
import mysql.connector

def submit():
    try:
     db=mysql.connector.connect(
     host="localhost",
     user="Layan",
     passwd="123456",
     database="imgsysdb"
     )
     
     mycursor=db.cursor()
     mycursor.execute("CREATE TABLE IMAGE_OPS (operation_id INT AUTO_INCREMENT PRIMARY KEY, source_image VARCHAR(200), transformation VARCHAR(15), argument VARCHAR(50), destination_image VARCHAR(200), creation_date DATETIME DEFAULT CURRENT_TIMESTAMP  )")
     sql="INSERT INTO IMAGE_OPS (source_image, transformation, argument, destination_image)Values (%s, %s, %s, %s)"
     val=[(image_name, clicked.get(), entry_box.get(), destination_file )]
     mycursor.executemany(sql,val)
     db.commit()
     print(mycursor.rowcount,"record inserted successfully.")
    except mysql.connector.Error as error:
      print("Failed to insert into IMAGE_OPS table {}".format(error))
    finally: 
     if db.is_connected():
         mycursor.close()  
         db.close()
         print("mySQL connection is closed")
    
def apply_flipping():
    flip_axis= entry_box.get()
    if flip_axis=='x-axis':
       flipped_img= selected_img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    elif flip_axis=='y-axis':
        flipped_img= selected_img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    image_label_display(flipped_img)
    destination_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if destination_file:
        flipped_img.save(destination_file)
        print("file succefully saved here"+destination_file)
        submit()
 
          
def apply_cropping():
    crop_values= entry_box.get()
    print(crop_values)
     # Split the crop values into a list of integers
    try:
        crop_values = list(map(int, crop_values.split(',')))
    except ValueError:
        messagebox.showerror(title="Error", message="Invalid crop values. Please enter four integers separated by commas.")
        return

    if len(crop_values) != 4:
        messagebox.showerror(title="Error", message="Invalid number of crop values. Please enter exactly four integers separated by commas.")
        return
    cropped_img= selected_img.crop((crop_values))
    image_label_display(cropped_img)
    destination_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if destination_file:
        cropped_img.save(destination_file)
        print("file succefully saved here"+destination_file)
        submit()
        
def apply_rotation():
    global destination_file
    rotation_value= int(entry_box.get())
    rotated_img= selected_img.rotate(rotation_value,expand=True)
    image_label_display(rotated_img)
    destination_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if destination_file:
        rotated_img.save(destination_file)
        print("file succefully saved here"+destination_file)
        submit()
        
def validate_rotation(new_value):
            new_value= entry_box.get()
            if new_value.isdigit():
                rotation_value = int(new_value) 
                if 0 <= rotation_value <= 360:
                  entry_box.config(highlightbackground="green")
                  transform_button=tk.Button(master=frame,text='apply', command=apply_rotation)
                  transform_button.grid(row=3,column=3,padx=15,pady=15)
                  return new_value
                else: messagebox.showerror(title="error", message="the range of rotation is between 0 to 360 degrees")
            elif new_value == "":
                entry_box.config(highlightbackground=None)
                return True  # Allow empty input
            else:
                messagebox.showerror(title="error", message="the input should be numbers")
                return False
  
# import mysql.connector
def display_entry(choice):
    global entry_box
    choice= clicked.get()
    if choice!= 'Select':
            entry_box = tk.Entry(frame)
            entry_box.grid(row=3, column=1)
            entry_box.focus_set()
            if choice =='Rotation':
                vcmd = (frame.register(validate_rotation), "%P")
                entry_box.config(validate="key", validatecommand=vcmd )
            elif choice=="Cropping":
                transform_button=tk.Button(master=frame,text='apply', command=apply_cropping)
                transform_button.grid(row=3,column=3,padx=15,pady=15)
            elif choice=="Flipping" :
                transform_button=tk.Button(master=frame,text='apply', command=apply_flipping)
                transform_button.grid(row=3,column=3,padx=15,pady=15)
                
def image_label_display(img):
     global desplayed_img, img_label
     img_label = None
     img=img.resize((300,300))
     desplayed_img=ImageTk.PhotoImage(img)
     if img_label:
            img_label.destroy()
     img_label= tk.Label(master=frame, image= desplayed_img, width=300, height=300)
     img_label.grid(row=2,column=0, padx=10, pady=10)               
            
def uploadImage():
    global image_name,selected_img,clicked
    image_types=[('png files','*.png'),('jpg files','*.jpg')]
    image_name= filedialog.askopenfilename(filetypes=image_types)
    print("this is image",image_name)
    if(image_name):
        selected_img= Image.open(image_name)
        image_label_display(selected_img)
        operation_list=['Select','Flipping', 'Rotation', 'Cropping']
        clicked= StringVar()
        clicked.set(operation_list[0])
        action_dropdown= tk.OptionMenu( frame, clicked,*operation_list,command=display_entry)
        action_dropdown.grid(row=3, column= 0 ,pady=0, padx=0)
          
window=tk.Tk()
window.title("Image transformer")
frame=tk.Frame(master=window,height=600, width=600)
frame.grid(row=0,column=0,padx=10,pady=10)
upload_button=tk.Button(master=frame,text='Upload Image', command=uploadImage)     
upload_button.grid(row=0,column=0,padx=15,pady=15)
window.mainloop()


        
    






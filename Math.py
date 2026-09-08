import random
import tkinter as tk
from tkinter import ttk




class MathTrainer:
 def __init__(self, root):
     self.root = root
     self.root.title("Math Dashboard")
     self.root.state('zoomed')
     self.root.configure(bg='lightblue')




     self.title_label = tk.Label(root, text="Math Game Dashboard", font=("Arial", 24), bg='lightblue')
     self.title_label.pack(pady=10)




     self.frame = tk.Frame(root, bg='lightblue')
     self.frame.pack()




     # Top Row Buttons
     tk.Button(self.frame, text="Addition (0-20)", font=("Arial", 18), width=20, height=2,
               command=self.open_addition_screen).grid(row=0, column=0, padx=10, pady=5)
     tk.Button(self.frame, text="Random within 10", font=("Arial", 18), width=20, height=2,
               command=self.open_random_within_10_screen).grid(row=0, column=1, padx=10, pady=5)
     tk.Button(self.frame, text="Random via 10", font=("Arial", 18), width=20, height=2,
               command=self.open_random_via_10_screen).grid(row=0, column=2, padx=10, pady=5)
     tk.Button(self.frame, text="Минус у 2х значных чисел", font=("Arial", 18), width=20, height=2,
               command=self.open_two_digit_subtraction_screen).grid(row=0, column=3, padx=10, pady=5)
     tk.Button(self.frame, text="Минус с отрицательным результатом", font=("Arial", 18), width=20, height=2,
               command=self.open_negative_result_subtraction_screen).grid(row=0, column=4, padx=10, pady=5)




     # Deduction Buttons
     for i in range(1, 10):
         tk.Button(self.frame, text=f"Deduction [0-20] - {i}", font=("Arial", 18), width=20, height=2,
                   command=self.make_deduction_screen_callback(i)).grid(row=i, column=1, padx=10, pady=5)
         tk.Button(self.frame, text=f"Deduction via 10 - {i}", font=("Arial", 18), width=20, height=2,
                   command=self.make_deduction1020_callback(i)).grid(row=i, column=2, padx=10, pady=5)




     tk.Button(self.frame, text="Минус: 1-значное из 2-значного", font=("Arial", 18), width=20, height=2,
               command=self.open_no_borrow_subtraction_screen).grid(row=10, column=0, padx=10, pady=5)




 def open_addition_screen(self):
     addition_window = tk.Toplevel(self.root)
     AdditionScreen(addition_window)




 def open_random_within_10_screen(self):
     random_window = tk.Toplevel(self.root)
     RandomWithin10Screen(random_window)




 def open_random_via_10_screen(self):
     random_window = tk.Toplevel(self.root)
     RandomVia10Screen(random_window)




 def open_two_digit_subtraction_screen(self):
     subtraction_window = tk.Toplevel(self.root)
     TwoDigitSubtractionScreen(subtraction_window)




 def open_negative_result_subtraction_screen(self):
     negative_result_window = tk.Toplevel(self.root)
     NegativeResultSubtractionScreen(negative_result_window)




 def open_no_borrow_subtraction_screen(self):
     no_borrow_window = tk.Toplevel(self.root)
     NoBorrowSubtractionScreen(no_borrow_window)




 def make_deduction_screen_callback(self, max_number):
     return lambda: self.open_deduction_screen(max_number)




 def open_deduction_screen(self, max_number):
     deduction_window = tk.Toplevel(self.root)
     DeductionScreen(deduction_window, max_number)




 def make_deduction1020_callback(self, max_number):
     return lambda: self.open_deduction1020_screen(max_number)




 def open_deduction1020_screen(self, max_number):
     deduction_window = tk.Toplevel(self.root)
     Deduction1020Screen(deduction_window, max_number)




class Deduction1020Screen:
 def __init__(self, root, max_number):
     self.root = root
     self.max_number = max_number
     self.root.title(f"Deduction via 10 - {max_number}")
     self.root.geometry("500x700")
     self.root.configure(bg='lightblue')




     self.back_button = tk.Button(root, text="Back", font=("Arial", 16), command=self.go_back)
     self.back_button.pack(pady=10, anchor='nw', padx=10)




     self.question_label = tk.Label(root, text="", font=("Arial", 32), bg='lightblue')
     self.question_label.pack(pady=10)




     self.buttons_frame = tk.Frame(root, bg='lightblue')
     self.buttons_frame.pack(pady=20)




     self.option_buttons = []
     for _ in range(8):
         button = tk.Button(self.buttons_frame, text="", font=("Arial", 24), width=5, height=2)
         button.grid(row=_//4, column=_%4, padx=10, pady=10)
         self.option_buttons.append(button)




     self.result_label = tk.Label(root, text="", font=("Arial", 24), bg='lightblue')
     self.result_label.pack(pady=20)




     self.stats_label = tk.Label(root, text="Correct: 0 | Incorrect: 0", font=("Arial", 20), bg='lightblue')
     self.stats_label.pack(pady=10)




     self.reset_button = tk.Button(root, text="Сбросить", font=("Arial", 16), command=self.reset_stats)
     self.reset_button.pack(pady=5)




     self.correct_answer = 0
     self.answers = []
     self.correct_count = 0
     self.incorrect_count = 0
     self.previous_a = None




     self.next_question()




 def go_back(self):
     self.root.destroy()




 def reset_stats(self):
     self.correct_count = 0
     self.incorrect_count = 0
     self.update_stats()




 def generate_question(self):
     b = self.max_number
     tries = 0
     while True:
         a = random.randint(11, 20)
         result = a - b
         if result < 10 and (self.previous_a is None or a != self.previous_a):
             break
         tries += 1
         if tries > 100:
             break
     self.previous_a = a
     self.num1 = a
     self.num2 = b
     self.correct_answer = result




 def next_question(self):
     self.generate_question()
     self.question_label.config(text=f"{self.num1} - {self.num2} = ?")
     self.result_label.config(text="")




     wrong_answers = set()
     attempts = 0
     while len(wrong_answers) < 7 and attempts < 100:
         delta = random.choice(range(-5, 6))
         wrong_answer = self.correct_answer + delta
         if 0 < wrong_answer < 10 and wrong_answer != self.correct_answer:
             wrong_answers.add(wrong_answer)
         attempts += 1




     while len(wrong_answers) < 7:
         wrong_answer = random.randint(1, 9)
         if wrong_answer != self.correct_answer:
             wrong_answers.add(wrong_answer)




     self.answers = list(wrong_answers)
     self.answers.append(self.correct_answer)
     random.shuffle(self.answers)




     for idx, button in enumerate(self.option_buttons):
         button.config(text=str(self.answers[idx]), command=lambda ans=self.answers[idx]: self.check_answer(ans), state='normal')




 def check_answer(self, selected_answer):
     if selected_answer == self.correct_answer:
         self.correct_count += 1
         self.result_label.config(text="Correct! Well done!", fg='green')
         self.update_stats()
         for button in self.option_buttons:
             button.config(state='disabled')
         self.root.after(1000, self.next_question)
     else:
         self.incorrect_count += 1
         self.result_label.config(text=f"Incorrect. The correct answer is: {self.correct_answer}", fg='red')
         self.update_stats()




 def update_stats(self):
     self.stats_label.config(text=f"Correct: {self.correct_count} | Incorrect: {self.incorrect_count}")




class AdditionScreen:
 def __init__(self, root):
     self.root = root
     self.root.title("Learn to Add!")
     self.root.geometry("500x700")
     self.root.configure(bg='lightblue')




     self.back_button = tk.Button(root, text="Back", font=("Arial", 16), command=self.go_back)
     self.back_button.pack(pady=10, anchor='nw', padx=10)




     self.question_label = tk.Label(root, text="", font=("Arial", 32), bg='lightblue')
     self.question_label.pack(pady=10)




     self.buttons_frame = tk.Frame(root, bg='lightblue')
     self.buttons_frame.pack(pady=20)




     self.option_buttons = []
     for _ in range(8):
         button = tk.Button(self.buttons_frame, text="", font=("Arial", 24), width=5, height=2)
         button.grid(row=_//4, column=_%4, padx=10, pady=10)
         self.option_buttons.append(button)




     self.result_label = tk.Label(root, text="", font=("Arial", 24), bg='lightblue')
     self.result_label.pack(pady=20)




     self.stats_label = tk.Label(root, text="Correct: 0 | Incorrect: 0", font=("Arial", 20), bg='lightblue')
     self.stats_label.pack(pady=10)




     self.reset_button = tk.Button(root, text="Сбросить", font=("Arial", 16), command=self.reset_stats)
     self.reset_button.pack(pady=5)




     self.num1 = 0
     self.num2 = 0
     self.correct_answer = 0
     self.answers = []
     self.correct_count = 0
     self.incorrect_count = 0




     self.next_question()




 def go_back(self):
     self.root.destroy()




 def reset_stats(self):
     self.correct_count = 0
     self.incorrect_count = 0
     self.update_stats()




 def generate_question_via(self):
   while True:
      firstDegree = random.randint(1, 8)
      secondDegree = random.randint(1, 8)
      if secondDegree + firstDegree > 10:
          continue
      a = random.randint(1, 9)
      diff = 10 - a
      b = random.randint(diff, 9)
      self.num1 = a + firstDegree * 10
      self.num2 = b + secondDegree * 10
      self.correct_answer = self.num1 + self.num2
      if self.correct_answer < 100:
          break


 def generate_question_within(self):
     while True:
         num1_ten = random.randint(1, 9)
         num2_ten = random.randint(1, 8)
         if num2_ten + num1_ten >= 10:
             continue
         # in ?X + ?Y, X+Y < 10
         num1_one = random.randint(1, 9)
         one_diff = 10 - num1_one


         num2_one = random.randint(1, one_diff)
         self.num1 = num1_one + num1_ten * 10
         self.num2 = num2_one + num2_ten * 10
         self.correct_answer = self.num1 + self.num2
         if self.correct_answer < 100:
             break


 def next_question(self):
     if random.randint(1, 6) < 5:
         self.generate_question_via()
     else:
         self.generate_question_within()


     self.question_label.config(text=f"{self.num1} + {self.num2} = ?")
     self.result_label.config(text="")


     wrong_answers = set([self.correct_answer-10, self.correct_answer+10])
     attempts = 0
     while len(wrong_answers) < 7 and attempts < 100:
         delta = random.choice([-11, -20, -2, -1, 1, 2, 11, 20])
         wrong_answer = self.correct_answer + delta
         if wrong_answer >= 0 and wrong_answer != self.correct_answer:
             wrong_answers.add(wrong_answer)
         attempts += 1




     while len(wrong_answers) < 7:
         wrong_answer = random.randint(0, 40)
         if wrong_answer != self.correct_answer:
             wrong_answers.add(wrong_answer)




     self.answers = list(wrong_answers)
     self.answers.append(self.correct_answer)
     random.shuffle(self.answers)




     for idx, button in enumerate(self.option_buttons):
         button.config(text=str(self.answers[idx]), command=lambda ans=self.answers[idx]: self.check_answer(ans), state='normal')




 def check_answer(self, selected_answer):
     if selected_answer == self.correct_answer:
         self.correct_count += 1
         self.result_label.config(text="Correct! Well done!", fg='green')
         self.update_stats()
         for button in self.option_buttons:
             button.config(state='disabled')
         self.root.after(1000, self.next_question)
     else:
         self.incorrect_count += 1
         self.result_label.config(text=f"Incorrect. The correct answer is: {self.correct_answer}", fg='red')
         self.update_stats()




 def update_stats(self):
     self.stats_label.config(text=f"Correct: {self.correct_count} | Incorrect: {self.incorrect_count}")




class RandomWithin10Screen:
 def __init__(self, root):
     self.root = root
     self.root.title("Random within 10")
     self.root.geometry("500x700")
     self.root.configure(bg='lightblue')




     self.back_button = tk.Button(root, text="Back", font=("Arial", 16), command=self.go_back)
     self.back_button.pack(pady=10, anchor='nw', padx=10)




     self.question_label = tk.Label(root, text="", font=("Arial", 32), bg='lightblue')
     self.question_label.pack(pady=10)




     self.buttons_frame = tk.Frame(root, bg='lightblue')
     self.buttons_frame.pack(pady=20)




     self.option_buttons = []
     for _ in range(8):
         button = tk.Button(self.buttons_frame, text="", font=("Arial", 24), width=5, height=2)
         button.grid(row=_//4, column=_%4, padx=10, pady=10)
         self.option_buttons.append(button)




     self.result_label = tk.Label(root, text="", font=("Arial", 24), bg='lightblue')
     self.result_label.pack(pady=20)




     self.stats_label = tk.Label(root, text="Correct: 0 | Incorrect: 0", font=("Arial", 20), bg='lightblue')
     self.stats_label.pack(pady=10)




     self.reset_button = tk.Button(root, text="Сбросить", font=("Arial", 16), command=self.reset_stats)
     self.reset_button.pack(pady=5)




     self.correct_answer = 0
     self.answers = []
     self.correct_count = 0
     self.incorrect_count = 0
     self.previous_a = None




     self.next_question()




 def go_back(self):
     self.root.destroy()




 def reset_stats(self):
     self.correct_count = 0
     self.incorrect_count = 0
     self.update_stats()




 def generate_question(self):
     tries = 0
     while True:
         a = random.randint(1, 30)
         b = random.randint(1, 9)
         result = a - b




         if a <= b:
             tries += 1
             if tries > 100:
                 break
             continue
         if 10 <= a <= 20 and not (10 <= result <= 20):
             tries += 1
             if tries > 100:
                 break
             continue
         if 21 <= a <= 30 and not (20 <= result <= 30):
             tries += 1
             if tries > 100:
                 break
             continue
         if self.previous_a is not None and a == self.previous_a:
             tries += 1
             if tries > 100:
                 break
             continue
         break




     self.previous_a = a
     self.num1 = a
     self.num2 = b
     self.correct_answer = result




 def next_question(self):
     self.generate_question()
     self.question_label.config(text=f"{self.num1} - {self.num2} = ?")
     self.result_label.config(text="")




     wrong_answers = set()
     attempts = 0
     while len(wrong_answers) < 7 and attempts < 100:
         delta = random.choice(range(-5, 6))
         wrong_answer = self.correct_answer + delta
         if wrong_answer > 0 and wrong_answer != self.correct_answer:
             wrong_answers.add(wrong_answer)
         attempts += 1




     while len(wrong_answers) < 7:
         wrong_answer = random.randint(1, 40)
         if wrong_answer != self.correct_answer:
             wrong_answers.add(wrong_answer)




     self.answers = list(wrong_answers)
     self.answers.append(self.correct_answer)
     random.shuffle(self.answers)




     for idx, button in enumerate(self.option_buttons):
         button.config(text=str(self.answers[idx]), command=lambda ans=self.answers[idx]: self.check_answer(ans), state='normal')




 def check_answer(self, selected_answer):
     if selected_answer == self.correct_answer:
         self.correct_count += 1
         self.result_label.config(text="Correct! Well done!", fg='green')
         self.update_stats()
         for button in self.option_buttons:
             button.config(state='disabled')
         self.root.after(1000, self.next_question)
     else:
         self.incorrect_count += 1
         self.result_label.config(text=f"Incorrect. The correct answer is: {self.correct_answer}", fg='red')
         self.update_stats()




 def update_stats(self):
     self.stats_label.config(text=f"Correct: {self.correct_count} | Incorrect: {self.incorrect_count}")




class RandomVia10Screen:
 def __init__(self, root):
     self.root = root
     self.root.title("Random via 10")
     self.root.geometry("500x700")
     self.root.configure(bg='lightblue')




     self.back_button = tk.Button(root, text="Back", font=("Arial", 16), command=self.go_back)
     self.back_button.pack(pady=10, anchor='nw', padx=10)




     self.question_label = tk.Label(root, text="", font=("Arial", 32), bg='lightblue')
     self.question_label.pack(pady=10)




     self.buttons_frame = tk.Frame(root, bg='lightblue')
     self.buttons_frame.pack(pady=20)




     self.option_buttons = []
     for _ in range(8):
         button = tk.Button(self.buttons_frame, text="", font=("Arial", 24), width=5, height=2)
         button.grid(row=_//4, column=_%4, padx=10, pady=10)
         self.option_buttons.append(button)




     self.result_label = tk.Label(root, text="", font=("Arial", 24), bg='lightblue')
     self.result_label.pack(pady=20)




     self.stats_label = tk.Label(root, text="Correct: 0 | Incorrect: 0", font=("Arial", 20), bg='lightblue')
     self.stats_label.pack(pady=10)




     self.reset_button = tk.Button(root, text="Сбросить", font=("Arial", 16), command=self.reset_stats)
     self.reset_button.pack(pady=5)




     self.correct_answer = 0
     self.answers = []
     self.correct_count = 0
     self.incorrect_count = 0
     self.previous_a = None




     self.next_question()




 def go_back(self):
     self.root.destroy()




 def reset_stats(self):
     self.correct_count = 0
     self.incorrect_count = 0
     self.update_stats()




 def generate_question(self):
     while True:
         num1_ten = random.randint(0, 9)
         num1_one = random.randint(1, 8)
         one_diff = 10 - num1_one


         num2_one = random.randint(one_diff, 10)
         self.num1 = num1_one + num1_ten * 10
         self.num2 = num2_one
         self.correct_answer = self.num1 - self.num2
         break


 def next_question(self):
     self.generate_question()
     self.question_label.config(text=f"{self.num1} - {self.num2} = ?")
     self.result_label.config(text="")




     wrong_answers = set()
     attempts = 0
     while len(wrong_answers) < 7 and attempts < 100:
         delta = random.choice(range(-5, 6))
         wrong_answer = self.correct_answer + delta
         if 0 < wrong_answer < 100 and wrong_answer != self.correct_answer:
             wrong_answers.add(wrong_answer)
         attempts += 1




     while len(wrong_answers) < 7:
         wrong_answer = random.randint(1, 40)
         if wrong_answer != self.correct_answer:
             wrong_answers.add(wrong_answer)




     self.answers = list(wrong_answers)
     self.answers.append(self.correct_answer)
     random.shuffle(self.answers)




     for idx, button in enumerate(self.option_buttons):
         button.config(text=str(self.answers[idx]), command=lambda ans=self.answers[idx]: self.check_answer(ans), state='normal')




 def check_answer(self, selected_answer):
     if selected_answer == self.correct_answer:
         self.correct_count += 1
         self.result_label.config(text="Correct! Well done!", fg='green')
         self.update_stats()
         for button in self.option_buttons:
             button.config(state='disabled')
         self.root.after(1000, self.next_question)
     else:
         self.incorrect_count += 1
         self.result_label.config(text=f"Incorrect. The correct answer is: {self.correct_answer}", fg='red')
         self.update_stats()




 def update_stats(self):
     self.stats_label.config(text=f"Correct: {self.correct_count} | Incorrect: {self.incorrect_count}")




class DeductionScreen:
 def __init__(self, root, max_number):
     self.root = root
     self.max_number = max_number
     self.root.title(f"Deduction - {max_number}")
     self.root.geometry("500x700")
     self.root.configure(bg='lightblue')




     self.back_button = tk.Button(root, text="Back", font=("Arial", 16), command=self.go_back)
     self.back_button.pack(pady=10, anchor='nw', padx=10)




     self.question_label = tk.Label(root, text="", font=("Arial", 32), bg='lightblue')
     self.question_label.pack(pady=10)




     self.buttons_frame = tk.Frame(root, bg='lightblue')
     self.buttons_frame.pack(pady=20)




     self.option_buttons = []
     for _ in range(8):
         button = tk.Button(self.buttons_frame, text="", font=("Arial", 24), width=5, height=2)
         button.grid(row=_//4, column=_%4, padx=10, pady=10)
         self.option_buttons.append(button)




     self.result_label = tk.Label(root, text="", font=("Arial", 24), bg='lightblue')
     self.result_label.pack(pady=20)




     self.stats_label = tk.Label(root, text="Correct: 0 | Incorrect: 0", font=("Arial", 20), bg='lightblue')
     self.stats_label.pack(pady=10)




     self.correct_answer = 0
     self.answers = []
     self.correct_count = 0
     self.incorrect_count = 0
     self.previous_a = None  # Track last minuend




     self.next_question()




 def go_back(self):
     self.root.destroy()




 def generate_question(self):
     b = self.max_number
     tries = 0
     while True:
         a = random.randint(b + 1, 20)
         if self.previous_a is None or a != self.previous_a:
             break
         tries += 1
         if tries > 100:  # Prevent infinite loop
             break
     self.previous_a = a
     self.num1 = a
     self.num2 = b
     self.correct_answer = self.num1 - self.num2




 def next_question(self):
     self.generate_question()
     self.question_label.config(text=f"{self.num1} - {self.num2} = ?")
     self.result_label.config(text="")




     wrong_answers = set()
     attempts = 0
     while len(wrong_answers) < 7 and attempts < 100:
         delta = random.choice(range(-5, 6))
         wrong_answer = self.correct_answer + delta
         if wrong_answer > 0 and wrong_answer != self.correct_answer:
             wrong_answers.add(wrong_answer)
         attempts += 1




     while len(wrong_answers) < 7:
         wrong_answer = random.randint(
             max(1, self.correct_answer - 10),
             self.correct_answer + 10
         )
         if wrong_answer != self.correct_answer:
             wrong_answers.add(wrong_answer)




     self.answers = list(wrong_answers)
     self.answers.append(self.correct_answer)
     random.shuffle(self.answers)




     for idx, button in enumerate(self.option_buttons):
         button.config(text=str(self.answers[idx]), command=lambda ans=self.answers[idx]: self.check_answer(ans), state='normal')




 def check_answer(self, selected_answer):
     if selected_answer == self.correct_answer:
         self.correct_count += 1
         self.result_label.config(text="Correct! Well done!", fg='green')
         self.update_stats()
         for button in self.option_buttons:
             button.config(state='disabled')
         self.root.after(1000, self.next_question)
     else:
         self.incorrect_count += 1
         self.result_label.config(text=f"Incorrect. The correct answer is: {self.correct_answer}", fg='red')
         self.update_stats()




 def update_stats(self):
     self.stats_label.config(text=f"Correct: {self.correct_count} | Incorrect: {self.incorrect_count}")




class TwoDigitSubtractionScreen:
 def __init__(self, root):
     self.root = root
     self.root.title("Минус у 2х значных чисел")
     self.root.geometry("500x700")
     self.root.configure(bg='lightblue')




     self.back_button = tk.Button(root, text="Back", font=("Arial", 16), command=self.go_back)
     self.back_button.pack(pady=10, anchor='nw', padx=10)




     self.question_label = tk.Label(root, text="", font=("Arial", 32), bg='lightblue')
     self.question_label.pack(pady=10)




     self.buttons_frame = tk.Frame(root, bg='lightblue')
     self.buttons_frame.pack(pady=20)




     self.option_buttons = []
     for _ in range(6):
         button = tk.Button(self.buttons_frame, text="", font=("Arial", 24), width=5, height=2)
         button.grid(row=_//3, column=_%3, padx=10, pady=10)
         self.option_buttons.append(button)




     self.result_label = tk.Label(root, text="", font=("Arial", 24), bg='lightblue')
     self.result_label.pack(pady=20)




     self.stats_frame = tk.Frame(root, bg='lightblue')
     self.stats_frame.pack(pady=10)




     self.correct_count = 0
     self.incorrect_count = 0
     self.correct_stats_label = tk.Label(self.stats_frame, text=f"Correct: {self.correct_count}", font=("Arial", 20), bg='lightblue', fg='green')
     self.correct_stats_label.pack(side='left', padx=10)
     self.incorrect_stats_label = tk.Label(self.stats_frame, text=f"Incorrect: {self.incorrect_count}", font=("Arial", 20), bg='lightblue', fg='red')
     self.incorrect_stats_label.pack(side='left', padx=10)




     self.correct_answer = 0
     self.answers = []




     self.next_question()




 def go_back(self):
     self.root.destroy()




 def generate_question(self):
     require_borrow = random.random() < 0.9
     tries = 0
     while True:
         tens1 = random.randint(1, 9)
         units1 = random.randint(0, 9)
         tens2 = random.randint(1, 9)
         units2 = random.randint(0, 9)
         num1 = tens1 * 10 + units1
         num2 = tens2 * 10 + units2
         result = num1 - num2
         units_diff = units1 - units2
         tries += 1
         if result <= 0:
             if tries > 200:
                 break
             continue
         if require_borrow and units_diff >= 0:
             if tries > 200:
                 break
             continue
         if not require_borrow and units_diff < 0:
             if tries > 200:
                 break
             continue
         break
     self.num1 = num1
     self.num2 = num2
     self.correct_answer = result




 def next_question(self):
     self.generate_question()
     self.question_label.config(text=f"{self.num1} - {self.num2} = ?")
     self.result_label.config(text="")




     wrong_answers = [self.correct_answer + delta for delta in (1, 10, 11, -1, -10)]
     wrong_answers = [value if value >= 0 else self.correct_answer + random.randint(2, 5) for value in wrong_answers]
     self.answers = wrong_answers + [self.correct_answer]
     random.shuffle(self.answers)




     for idx, button in enumerate(self.option_buttons):
         button.config(text=str(self.answers[idx]), command=lambda ans=self.answers[idx]: self.check_answer(ans), state='normal')




 def check_answer(self, selected_answer):
     for button in self.option_buttons:
         button.config(state='disabled')
     if selected_answer == self.correct_answer:
         self.result_label.config(text="Correct! Well done!", fg='green')
         self.root.after(2000, lambda: self.finish_turn(True))
     else:
         self.result_label.config(text=f"Incorrect. The correct answer is: {self.correct_answer}", fg='red')
         self.root.after(2000, lambda: self.finish_turn(False))




 def finish_turn(self, was_correct):
     if was_correct:
         self.correct_count += 1
     else:
         self.incorrect_count += 1
     self.update_stats()
     self.next_question()




 def update_stats(self):
     self.correct_stats_label.config(text=f"Correct: {self.correct_count}")
     self.incorrect_stats_label.config(text=f"Incorrect: {self.incorrect_count}")


class NegativeResultSubtractionScreen:
 def __init__(self, root):
     self.root = root
     self.root.title("Минус с отрицательным результатом")
     self.root.geometry("500x700")
     self.root.configure(bg='lightblue')




     self.back_button = tk.Button(root, text="Back", font=("Arial", 16), command=self.go_back)
     self.back_button.pack(pady=10, anchor='nw', padx=10)




     self.question_label = tk.Label(root, text="", font=("Arial", 32), bg='lightblue')
     self.question_label.pack(pady=10)




     self.buttons_frame = tk.Frame(root, bg='lightblue')
     self.buttons_frame.pack(pady=20)




     self.option_buttons = []
     for _ in range(6):
         button = tk.Button(self.buttons_frame, text="", font=("Arial", 24), width=5, height=2)
         button.grid(row=_//3, column=_%3, padx=10, pady=10)
         self.option_buttons.append(button)




     self.result_label = tk.Label(root, text="", font=("Arial", 24), bg='lightblue')
     self.result_label.pack(pady=20)




     self.stats_frame = tk.Frame(root, bg='lightblue')
     self.stats_frame.pack(pady=10)




     self.correct_count = 0
     self.incorrect_count = 0
     self.correct_stats_label = tk.Label(self.stats_frame, text=f"Correct: {self.correct_count}", font=("Arial", 20), bg='lightblue', fg='green')
     self.correct_stats_label.pack(side='left', padx=10)
     self.incorrect_stats_label = tk.Label(self.stats_frame, text=f"Incorrect: {self.incorrect_count}", font=("Arial", 20), bg='lightblue', fg='red')
     self.incorrect_stats_label.pack(side='left', padx=10)




     self.correct_answer = 0
     self.answers = []




     self.next_question()




 def go_back(self):
     self.root.destroy()




 def generate_question(self):
     num1 = random.randint(1, 9)
     tens2 = random.randint(1, 9)
     units2 = random.randint(0, 9)
     num2 = tens2 * 10 + units2
     self.num1 = num1
     self.num2 = num2
     self.correct_answer = num1 - num2




 def next_question(self):
     self.generate_question()
     self.question_label.config(text=f"{self.num1} - {self.num2} = ?")
     self.result_label.config(text="")




     wrong_answers = [self.correct_answer + delta for delta in (1, 10, 11, -1, -10)]
     self.answers = wrong_answers + [self.correct_answer]
     random.shuffle(self.answers)




     for idx, button in enumerate(self.option_buttons):
         button.config(text=str(self.answers[idx]), command=lambda ans=self.answers[idx]: self.check_answer(ans), state='normal')




 def check_answer(self, selected_answer):
     for button in self.option_buttons:
         button.config(state='disabled')
     if selected_answer == self.correct_answer:
         self.result_label.config(text="Correct! Well done!", fg='green')
         self.root.after(2000, lambda: self.finish_turn(True))
     else:
         self.result_label.config(text=f"Incorrect. The correct answer is: {self.correct_answer}", fg='red')
         self.root.after(2000, lambda: self.finish_turn(False))




 def finish_turn(self, was_correct):
     if was_correct:
         self.correct_count += 1
     else:
         self.incorrect_count += 1
     self.update_stats()
     self.next_question()




 def update_stats(self):
     self.correct_stats_label.config(text=f"Correct: {self.correct_count}")
     self.incorrect_stats_label.config(text=f"Incorrect: {self.incorrect_count}")


class NoBorrowSubtractionScreen:
 def __init__(self, root):
     self.root = root
     self.root.title("Минус: 1-значное из 2-значного")
     self.root.geometry("500x700")
     self.root.configure(bg='lightblue')




     self.back_button = tk.Button(root, text="Back", font=("Arial", 16), command=self.go_back)
     self.back_button.pack(pady=10, anchor='nw', padx=10)




     self.question_label = tk.Label(root, text="", font=("Arial", 32), bg='lightblue')
     self.question_label.pack(pady=10)




     self.buttons_frame = tk.Frame(root, bg='lightblue')
     self.buttons_frame.pack(pady=20)




     self.option_buttons = []
     for _ in range(6):
         button = tk.Button(self.buttons_frame, text="", font=("Arial", 24), width=5, height=2)
         button.grid(row=_//3, column=_%3, padx=10, pady=10)
         self.option_buttons.append(button)




     self.result_label = tk.Label(root, text="", font=("Arial", 24), bg='lightblue')
     self.result_label.pack(pady=20)




     self.stats_frame = tk.Frame(root, bg='lightblue')
     self.stats_frame.pack(pady=10)




     self.correct_count = 0
     self.incorrect_count = 0
     self.correct_stats_label = tk.Label(self.stats_frame, text=f"Correct: {self.correct_count}", font=("Arial", 20), bg='lightblue', fg='green')
     self.correct_stats_label.pack(side='left', padx=10)
     self.incorrect_stats_label = tk.Label(self.stats_frame, text=f"Incorrect: {self.incorrect_count}", font=("Arial", 20), bg='lightblue', fg='red')
     self.incorrect_stats_label.pack(side='left', padx=10)




     self.correct_answer = 0
     self.answers = []




     self.next_question()




 def go_back(self):
     self.root.destroy()




 def generate_question(self):
     num1 = random.randint(1, 9)
     tens2 = random.randint(1, 9)
     units2 = random.randint(num1, 9)  # units2 >= num1: no borrow across the tens digit
     num2 = tens2 * 10 + units2
     self.num1 = num1
     self.num2 = num2
     self.correct_answer = num1 - num2




 def next_question(self):
     self.generate_question()
     self.question_label.config(text=f"{self.num1} - {self.num2} = ?")
     self.result_label.config(text="")




     wrong_answers = [self.correct_answer + delta for delta in (1, 10, 11, -1, -10)]
     self.answers = wrong_answers + [self.correct_answer]
     random.shuffle(self.answers)




     for idx, button in enumerate(self.option_buttons):
         button.config(text=str(self.answers[idx]), command=lambda ans=self.answers[idx]: self.check_answer(ans), state='normal')




 def check_answer(self, selected_answer):
     for button in self.option_buttons:
         button.config(state='disabled')
     if selected_answer == self.correct_answer:
         self.result_label.config(text="Correct! Well done!", fg='green')
         self.root.after(2000, lambda: self.finish_turn(True))
     else:
         self.result_label.config(text=f"Incorrect. The correct answer is: {self.correct_answer}", fg='red')
         self.root.after(2000, lambda: self.finish_turn(False))




 def finish_turn(self, was_correct):
     if was_correct:
         self.correct_count += 1
     else:
         self.incorrect_count += 1
     self.update_stats()
     self.next_question()




 def update_stats(self):
     self.correct_stats_label.config(text=f"Correct: {self.correct_count}")
     self.incorrect_stats_label.config(text=f"Incorrect: {self.incorrect_count}")



if __name__ == "__main__":
 try:
     root = tk.Tk()
     app = MathTrainer(root)
     root.mainloop()
 except ModuleNotFoundError:
     print("Tkinter is not available. Please run this script in an environment where Tkinter is installed.")







from flask import Flask, render_template, request, json
import logging
import git

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route ('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('6174-kaprekara')
        origin=repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

def numerics(n):
    return list(map(int, str(n)))

def kaprekar_step(L):
    max_num = int("".join(map(str, sorted(L, reverse=True))))
    min_num = int("".join(map(str, sorted(L))))
    return max_num - min_num, max_num, min_num

def get_999_difference_numbers():
    numbers_with_999_diff = []
    for i in range(1000, 10000):
        digit_list = numerics(i)
        diff, _, _ = kaprekar_step(digit_list)
        if diff == 999:
            numbers_with_999_diff.append(i)

    return numbers_with_999_diff

def print_999_difference_info():
    numbers_with_999_diff = get_999_difference_numbers()
    total_count = 9000
    count_with_999_diff = len(numbers_with_999_diff)
    percentage = (count_with_999_diff / total_count) * 100

    output_info = []
    output_info.append("Вы нашли число, которое не подчиняется этой последовательности, ниже все подобные числа:")
    output_info.append(str(numbers_with_999_diff))
    output_info.append("Можно сделать вывод, что все 4-значные числа, у которых крайние и средние цифры отличаются на 1, будут иметь разницу между максимальным и минимальным числами, равную 999.")
    output_info.append(f"Кол-во таких чисел: {count_with_999_diff}")
    output_info.append(f"Процент таких чисел: {percentage:.2f}%")

    other_numbers_count = total_count - count_with_999_diff
    other_numbers_percentage = (other_numbers_count / total_count) * 100

    output_info.append(f"Количество других 4-значных чисел: {other_numbers_count}")
    output_info.append(f"Процент других 4-значных чисел: {other_numbers_percentage:.2f}%")
    output_info.append(f"Всего 4-значных чисел: {total_count}")

    return output_info

def kaprekar_loop(n):
    steps = 0
    seen_numbers = set()
    results = []

    while n != 6174:
        if n in seen_numbers:
            results.append(f"Число {n} повторилось, цикл завершен.")
            break
        seen_numbers.add(n)
        steps += 1

        formatted_n = str(n).zfill(4)
        results.append(f"<div style='text-align:center;'>Шаг {steps}: {formatted_n}</div>")
        digit_list = numerics(n)
        diff, max_num, min_num = kaprekar_step(digit_list)

        results.append(f"<div style='text-align:center;'>{str(max_num).zfill(4)}</div>")
        results.append(f"<div style='text-align:center; text-decoration:underline;'>{str(min_num).zfill(4)}</div>")
        results.append(f"<div style='text-align:center;'>{str(diff).zfill(4)}</div>")

        n = diff

        if n == 0:
            results.append("<div style='text-align:center;'>⚠️ Число 0 не подходит для последовательности Капрекара.</div>")
            break

        elif n == 999:
            results.append("<div style='text-align:center;'>⚠️ Внимание: число 999 не подходит для последовательности Капрекара.</div>")
            number_info = print_999_difference_info()
            results.extend(number_info)
            break
        elif n == 495:
            results.append("<div style='text-align:center;'>🔄 Обратите внимание: Вы вводите трехзначное число.</div>")
            break

    if n == 6174:
        results.append(f"<div style='text-align:center;'>🎉 Шаг {steps}: {n}</div>")
        results.append("<div style='text-align:center;'>Мы достигли магического числа 6174!</div>")

    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        try:
            number = int(request.form['number'])
            if number < 1000 or number > 9999:
                results.append("<div style='text-align:center;'>⚠️ Пожалуйста, введите 4-значное число.</div>")
            else:
                results = kaprekar_loop(number)
        except ValueError:
            results.append("<div style='text-align:center;'>⚠️ Пожалуйста, введите корректное число.</div>")
    return render_template('index.html', results=results)

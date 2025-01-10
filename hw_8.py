# -*- coding: utf-8 -*-
"""ДЗ8_Кравченко Сергій.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TIlZSQZLeN6KZw_X2LAmFHwEa9-wAgbG

## Завдання 1

Візьми код симуляції із завдання 7 домашнього завдання до теми 7 “Теорія ймовірностей. Комбінаторика”. Будемо вважати, що зміна ціни акцій у кожний момент часу дорівнює
x
∼
Γ
(
0.3
,
1.1
)
x∼Γ(0.3,1.1), де

Г — позначення гамма-розподілу.



Необхідно запустити симуляцію
n
=
100
n=100 разів для різних значень часу
t.

а) Побудуй гістограму розподілу
x.

б) Запусти симуляцію з
t від 1 до, наприклад, ~60 з кроком, наприклад, 1 або 2.

Примітка: кінцеве значення t взято умовно рівним 60, але це не відіграє великої ролі, головне, щоб воно було достатнім для проходження тесту на нормальність, а значення кроку — дозволяло побачити динаміку зміни розподілу. Конкретні значення не так важливі.


Для кожного значення
t побудуй гістограму розподілу ціни та перевір його на нормальність. Зроби висновки про зміну розподілу зі збільшенням
t.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma, normaltest

# Параметри гамма-розподілу
shape, scale = 0.3, 1.1

# Симуляція однієї зміни ціни на основі гамма-розподілу
def stock_price_at_time_gamma(t):
    changes = gamma.rvs(a=shape, scale=scale, size=t)  # Генерація змін
    return np.sum(changes)

# Симуляція n разів для заданого t
def simulate_n_times_gamma(n, t):
    prices = [stock_price_at_time_gamma(t) for _ in range(n)]
    return prices

# Побудова гістограми розподілу x (змін ціни) для t = 1
x_changes = gamma.rvs(a=shape, scale=scale, size=1000)
plt.figure(figsize=(10, 6))
plt.hist(x_changes, bins=20, edgecolor='k', alpha=0.7)
plt.title('Гістограма розподілу змін ціни (гамма-розподіл)')
plt.xlabel('Зміна ціни')
plt.ylabel('Частота')
plt.grid(True)
plt.show()

# Запуск симуляції для t = 1 до t = 60 з кроком 2
t_values = range(1, 61, 2)
n = 100  # Кількість симуляцій для кожного t

for t in t_values:
    prices = simulate_n_times_gamma(n, t)
    mean_price = np.mean(prices)
    _, p_value = normaltest(prices)  # Тест на нормальність

    plt.figure(figsize=(10, 6))
    plt.hist(prices, bins=20, edgecolor='k', alpha=0.7)
    plt.title(f'Гістограма розподілу ціни для t={t}\nСередня ціна = {mean_price:.2f}, p-value = {p_value:.4f}')
    plt.xlabel('Ціна акцій')
    plt.ylabel('Частота')
    plt.grid(True)
    plt.show()

    # Висновок про нормальність розподілу
    if p_value > 0.05:
        print(f"Для t={t}: Розподіл можна вважати нормальним (p-value = {p_value:.4f})")
    else:
        print(f"Для t={t}: Розподіл значно відрізняється від нормального (p-value = {p_value:.4f})")

"""## Завдання 2

Завантаж набір даних Product Advertising Data (посилання на диск). Набір даних складається із семи стовпчиків, що відображають витрати на рекламу на різних платформах — телебачення, білборди, Google Ads, соціальні медіа, інфлюенс-маркетинг та партнерський маркетинг.



Останній стовпчик, "Product_Sold", містить кількісну оцінку відповідної кількості проданих одиниць товару. Для кожної колонки порахуй середнє значення, дисперсію, стандартне відхилення, побудуй гістограму розподілу показника, перевір на нормальність розподілу та порахуй кореляцію з Product_Sold.
"""

!pip install q kaggle
from google.colab import files
import pandas as pd
import numpy as np
from google.colab import autoviz
import seaborn as sns



# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')  # Remove if not accessing Google Drive

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, normaltest, pearsonr
from google.colab import files
import io
import os

# Download the CSV file with a specified filename
!gdown --id '1xxUxDZOafQ6ZNhX6Kfc3jvUcUtAZ2Kji' -O /content/Advertising_Data.csv

# Verify the download
data_path = '/content/Advertising_Data.csv'

if not os.path.exists(data_path):
    raise FileNotFoundError(f"File not found at {data_path}. Please check the file ID and try again.")
elif os.path.getsize(data_path) == 0:
    raise ValueError(f"The file {data_path} is empty. Please verify the file content.")
else:
    print(f"File {data_path} downloaded successfully.")

# Load the data
data = pd.read_csv(data_path)

# Display descriptive statistics
stats = data.describe()
print("Descriptive Statistics:")
print(stats)

# Calculate means, variances, and standard deviations
means = data.mean()
variances = data.var()
std_devs = data.std()

# Обчислення кореляцій з 'Product_Sold'
if 'Product_Sold' in data.columns:
    correlations = data.corr()['Product_Sold']
    print("\nКореляції з Product_Sold:")
    print(correlations)
else:
    print("Колонка 'Product_Sold' не знайдена в датасеті.")

# Виведення середніх значень, дисперсій та стандартних відхилень
print("\nСередні значення:")
print(means)
print("\nДисперсії:")
print(variances)
print("\nСтандартні відхилення:")
print(std_devs)

# Перевірка наявності колонки 'Product_Sold'
if 'Product_Sold' in data.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Product_Sold'], kde=True, bins=30, color='orange')
    plt.title('Гістограма Product_Sold')
    plt.xlabel('Product_Sold')
    plt.ylabel('Частота')
    plt.grid(True)
    plt.show()

    # Shapiro-Wilk Test для Product_Sold
    stat, p = shapiro(data['Product_Sold'])
    print(f'Shapiro-Wilk тест для Product_Sold: Statistics={stat:.4f}, p-value={p:.4f}')

    # D'Agostino's K^2 Test для Product_Sold
    stat, p = normaltest(data['Product_Sold'])
    print(f"D'Agostino's K^2 тест для Product_Sold: Statistics={stat:.4f}, p-value={p:.4f}")

    # Інтерпретація результатів
    if p < 0.05:
        print('Розподіл Product_Sold не є нормальним (p < 0.05)')
    else:
        print('Розподіл Product_Sold є нормальним (p >= 0.05)')
else:
    print("Колонка 'Product_Sold' не знайдена в датасеті.")

# **Аналіз інших колонок**
numerical_columns = data.select_dtypes(include=[np.number]).columns.tolist()

for column in numerical_columns:
    if column == 'Product_Sold':
        continue

    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], kde=True, bins=30)
    plt.title(f'Гістограма {column}')
    plt.xlabel(column)
    plt.ylabel('Частота')
    plt.grid(True)
    plt.show()

    # Shapiro-Wilk Test
    stat, p = shapiro(data[column])
    print(f'Shapiro-Wilk тест для {column}: Statistics={stat:.4f}, p-value={p:.4f}')

    # D'Agostino's K^2 Test
    stat, p = normaltest(data[column])
    print(f"D'Agostino's K^2 тест для {column}: Statistics={stat:.4f}, p-value={p:.4f}")

    # Інтерпретація результатів
    if p < 0.05:
        print(f'Розподіл {column} не є нормальним (p < 0.05)\n')
    else:
        print(f'Розподіл {column} є нормальним (p >= 0.05)\n')

# Візуалізація кореляційної матриці
plt.figure(figsize=(12, 10))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Кореляційна матриця')
plt.show()
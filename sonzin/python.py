import os
import shutil
import tkinter as tk
from tkinter import Button, filedialog
import pygame
import ctypes
import sys

# Função para ocultar o console ao executar o arquivo .exe
def hide_console_window():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Inicializa a janela principal
def initialize_window():
    root = tk.Tk()
    root.title("Reproduzir Som")
    root.geometry("600x180")
    return root

# Cores personalizadas
button_bg_color = "#4CAF50"  # Verde
button_fg_color = "#FFFFFF"  # Branco

# Diretório dos sons
sound_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")

# Verifica se o diretório de sons existe
if not os.path.isdir(sound_dir):
    print("Erro: O diretório de sons não existe.")
    sys.exit(1)

# Verifica se há arquivos de som no diretório
sound_files = [filename for filename in os.listdir(sound_dir) if filename.endswith(".mp3")]
if not sound_files:
    print("Erro: Não há arquivos de som no diretório.")
    sys.exit(1)

# Dicionário com os sons e seus atalhos correspondentes
def get_sounds_dict(sound_dir):
    sounds = {}
    for filename in sound_files:
        label = os.path.splitext(filename)[0]
        sounds[label] = {"file": os.path.abspath(os.path.join(sound_dir, filename)), "shortcut": label[-1]}
    return sounds

# Função para reproduzir o som com o pygame
def play_sound_pygame(label):
    sound_data = sounds[label]
    sound_file = sound_data["file"]
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# Função para trocar um som existente
def change_sound(label, new_file=None):
    try:
        if new_file is None:
            if getattr(sys, 'frozen', False):  # Verifica se está sendo executado como um executável
                new_file = input(f"Digite o caminho para o novo arquivo de som para {label}: ")
            else:
                new_file = filedialog.askopenfilename()
            if not new_file:
                print("Nenhum arquivo selecionado.")
                return

        # Obtém o nome do arquivo
        filename = os.path.basename(new_file)
        label = f"som_{label[-1]}.mp3"  # Mantém o mesmo nome do som existente
        new_sound_path = os.path.join(sound_dir, label)

        # Remove o arquivo de som existente se já houver um
        if os.path.exists(new_sound_path):
            os.remove(new_sound_path)

        # Move o novo arquivo para o diretório de sons
        shutil.move(new_file, new_sound_path)

        # Atualiza o dicionário de sons
        sounds[label] = {"file": new_sound_path, "shortcut": label[-1]}
        print(f"Som {label} trocado com sucesso.")
    except Exception as e:
        print(f"Erro ao trocar o som {label}: {e}")

# Função para inicializar o mixer do pygame
def initialize_pygame():
    pygame.mixer.init()

# Função para lidar com eventos de teclado
def handle_key_event(event):
    key = event.char
    if key.isdigit():
        label = f"som_{key}.mp3"
        if label in sounds:
            play_sound_pygame(label)

# Cria a interface gráfica
def create_gui():
    global sounds_list  # Define sounds_list como global
    sounds_list = list(sounds.keys())  # Define sounds_list como uma lista global
    # Adiciona botões para cada som na interface
    for label in sounds_list:
        create_sound_button(label)

# Função para criar botões de som na interface
def create_sound_button(label):
    button = Button(root, text=label, width=15, height=2, bg=button_bg_color, fg=button_fg_color,
                    font=("Arial", 10, "bold"), command=lambda l=label: play_sound_pygame(l))
    button.grid(row=0, column=sounds_list.index(label), padx=10, pady=10)

    change_button = Button(root, text=f"Trocar {label}", width=15, height=2, bg=button_bg_color, fg=button_fg_color,
                           font=("Arial", 10, "bold"), command=lambda l=label: change_sound(l))
    change_button.grid(row=1, column=sounds_list.index(label), padx=10, pady=5)

# Oculta o console ao executar o arquivo .exe
hide_console_window()

# Inicializa a janela principal
root = initialize_window()

# Inicializa o mixer do pygame
initialize_pygame()

# Obtém o dicionário de sons
sounds = get_sounds_dict(sound_dir)

# Cria a interface gráfica
create_gui()

# Associa a função de lidar com eventos de teclado
root.bind("<Key>", handle_key_event)

# Mantém a interface gráfica em execução
root.mainloop()

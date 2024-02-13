import tkinter as tk
from tkinter import ttk

is_paused = False
is_stopped = False

class Noeud:
    def __init__(self, valeur):
        self.valeur = valeur
        self.gauche = None
        self.droite = None

class ArbreBinaire:
    def __init__(self):
        self.racine = None
        self.ligne_ids = {} 

    def inserer(self, valeur):
        if self.racine is None:
            self.racine = Noeud(valeur)
        else:
            self._inserer(valeur, self.racine)

    def _inserer(self, valeur, noeud):
        if valeur < noeud.valeur:
            if noeud.gauche is None:
                noeud.gauche = Noeud(valeur)
            else:
                self._inserer(valeur, noeud.gauche)
        elif valeur > noeud.valeur:
            if noeud.droite is None:
                noeud.droite = Noeud(valeur)
            else:
                self._inserer(valeur, noeud.droite)

    def supprimer(self, valeur):
        self.racine = self._supprimer(self.racine, valeur)

    def _supprimer(self, noeud, valeur):
        if noeud is None:
            return noeud
        if valeur < noeud.valeur:
            noeud.gauche = self._supprimer(noeud.gauche, valeur)
        elif valeur > noeud.valeur:
            noeud.droite = self._supprimer(noeud.droite, valeur)
        else:
            if noeud.gauche is None:
                return noeud.droite
            elif noeud.droite is None:
                return noeud.gauche
            temp_noeud = self._min_value_node(noeud.droite)
            noeud.valeur = temp_noeud.valeur
            noeud.droite = self._supprimer(noeud.droite, temp_noeud.valeur)
        return noeud

    def _min_value_node(self, noeud):
        current = noeud
        while current.gauche is not None:
            current = current.gauche
        return current

    def dessiner(self, canvas, x, y, espace, noeud=None, color="white"):
        if noeud is None:
            noeud = self.racine
        if noeud is not None:
            canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline=color)
            canvas.create_text(x, y, text=str(noeud.valeur), font=('Arial', 12, 'bold'), fill="black")
            if noeud.gauche:
                ligne_id = canvas.create_line(x, y + 20, x - espace, y + 70, width=2, fill="black")
                self.ligne_ids[(noeud, noeud.gauche)] = ligne_id
                self.dessiner(canvas, x - espace, y + 70, espace/2, noeud.gauche, color)
            if noeud.droite:
                ligne_id = canvas.create_line(x, y + 20, x + espace, y + 70, width=2, fill="black")
                self.ligne_ids[(noeud, noeud.droite)] = ligne_id
                self.dessiner(canvas, x + espace, y + 70, espace/2, noeud.droite, color)

    def mettre_en_evidence(self, canvas, x, y, espace, noeud, parent_pos=None):
        global is_paused, is_stopped
        if noeud:
            # Mise à jour seulement du tronçon connecté au noeud actuel
            if parent_pos:
                parent_noeud = self._trouver_parent(noeud)
                ligne_id = self.ligne_ids.get((parent_noeud, noeud))
                if ligne_id:  # Si nous avons une ligne à mettre à jour
                    canvas.itemconfig(ligne_id, fill="#008888")  # Changer la couleur en rouge
            canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="#008888", outline="#008888")
            canvas.create_text(x, y, text=str(noeud.valeur), font=('Arial', 12, 'bold'), fill="black")
    
            # Vérification de l'état de l'animation
            while is_paused:
                canvas.update()
                if is_stopped:
                    return  # Sortir de la fonction si l'animation est arrêtée
    
            canvas.update()
            canvas.after(700)  # Pause pour ralentir l'animation


    def parcours_prefixe(self, noeud, resultat, canvas, x, y, espace, parent_pos=None):
        global is_paused, is_stopped
        if noeud and not is_stopped:
            self.mettre_en_evidence(canvas, x, y, espace, noeud, parent_pos)
            resultat.append(noeud.valeur)
    
            # Vérifiez si l'animation est en pause ou arrêtée avant de continuer
            while is_paused:
                canvas.update()
                if is_stopped:
                    return  # Sortir de la fonction si l'animation est arrêtée
    
            if noeud.gauche:
                self.parcours_prefixe(noeud.gauche, resultat, canvas, x - espace, y + 70, espace / 2, parent_pos=(x, y))
    
            # Vérifiez à nouveau si l'animation est en pause ou arrêtée avant de continuer
            while is_paused:
                canvas.update()
                if is_stopped:
                    return  # Sortir de la fonction si l'animation est arrêtée
    
            if noeud.droite:
                self.parcours_prefixe(noeud.droite, resultat, canvas, x + espace, y + 70, espace / 2, parent_pos=(x, y))

    def parcours_infixe(self, noeud, resultat, canvas, x, y, espace, parent_pos=None):
        global is_paused, is_stopped
        if noeud and not is_stopped:
            if noeud.gauche:
                self.parcours_infixe(noeud.gauche, resultat, canvas, x - espace, y + 70, espace / 2, parent_pos=(x, y))
    
            while is_paused:
                canvas.update()
                if is_stopped:
                    return
    
            self.mettre_en_evidence(canvas, x, y, espace, noeud, parent_pos)
            resultat.append(noeud.valeur)
    
            if noeud.droite:
                self.parcours_infixe(noeud.droite, resultat, canvas, x + espace, y + 70, espace / 2, parent_pos=(x, y))

    def parcours_postfixe(self, noeud, resultat, canvas, x, y, espace, parent_pos=None):
        global is_paused, is_stopped
        if noeud and not is_stopped:
            if noeud.gauche:
                self.parcours_postfixe(noeud.gauche, resultat, canvas, x - espace, y + 70, espace / 2, parent_pos=(x, y))
    
            while is_paused:
                canvas.update()
                if is_stopped:
                    return
    
            if noeud.droite:
                self.parcours_postfixe(noeud.droite, resultat, canvas, x + espace, y + 70, espace / 2, parent_pos=(x, y))
    
            self.mettre_en_evidence(canvas, x, y, espace, noeud, parent_pos)
            resultat.append(noeud.valeur)

    def position_noeud(self, noeud, x, y, espace):
        if noeud is None:
            return None
        queue = [(self.racine, x, y)]
        while queue:
            current, cur_x, cur_y = queue.pop(0)
            if current == noeud:
                return cur_x, cur_y
            if current.gauche:
                queue.append((current.gauche, cur_x - espace, cur_y + 70))
            if current.droite:
                queue.append((current.droite, cur_x + espace, cur_y + 70))
        return None
    
    def _trouver_parent(self, child):
        parent = None
        queue = [(self.racine, None)]
        while queue:
            current, current_parent = queue.pop(0)
            if current == child:
                return current_parent
            if current.gauche:
                queue.append((current.gauche, current))
            if current.droite:
                queue.append((current.droite, current))
        return parent


def main():
    root = tk.Tk()
    root.title("Manipulation d'un arbre binaire")
    arbre = ArbreBinaire()

    # Sidebar styling
    sidebar = tk.Frame(root, bg='#008888', width=600, height=600)  
    sidebar.pack(expand=False, fill='y', side='left', anchor='nw',)
 
    
    # Variables d'état pour l'animation
    is_paused = False
    is_stopped = False

    def pause_animation():
        global is_paused
        is_paused = True
    
    def resume_animation():
        global is_paused
        is_paused = False
    
    def stop_animation():
        global is_stopped, is_paused
        is_stopped = True
        is_paused = False
        
    def start_animation():
            global is_stopped, is_paused
            is_stopped = False
            is_paused = False
   
    # Modifier mettre_en_evidence pour vérifier l'état de l'animation
    def mettre_en_evidence(canvas, x, y, espace, noeud, parent_pos=None):
        if noeud:
            while is_paused:
                canvas.update()
                if is_stopped:
                    return  # Sortir de la fonction si l'animation est arrêtée
                
                
 # Ne pas pack les Entry widgets immédiatement
    valeur_insertion = tk.StringVar()
    entry_inserer = ttk.Entry(sidebar, textvariable=valeur_insertion, width=15)

    valeur_suppression = tk.StringVar()
    entry_supprimer = ttk.Entry(sidebar, textvariable=valeur_suppression, width=15)

    style = ttk.Style()
    style.configure('TButton', background='black', foreground='black', font=('Arial', 10), width=20, height=2)


    canvas = tk.Canvas(root, width=600, height=600, bg="white")
    canvas.pack(expand=True, fill='both', side='top')
    
    resultat_parcours = tk.StringVar(value="")
    label_resultat_parcours = tk.Label(sidebar, textvariable=resultat_parcours, bg='white', fg='black', width=25, anchor='w')

    def hide_widgets():
        # Cette fonction cache les widgets de résultat et les zones de texte d'insertion et de suppression
        label_resultat_parcours.pack_forget()
        entry_inserer.pack_forget()
        entry_supprimer.pack_forget()
        btn_inserer.pack_forget()
        btn_supprimer.pack_forget()
        valeur_insertion.set('')  # Efface la zone de texte d'insertion
        valeur_suppression.set('')  # Efface la zone de texte de suppression
        
    def show_entry_inserer():
        hide_widgets()  # Cache les autres widgets en premier
        entry_inserer.pack(pady=10)
        btn_inserer.pack(pady=10)
    
    def show_entry_supprimer():
        hide_widgets()  # Cache les autres widgets en premier
        entry_supprimer.pack(pady=10)
        btn_supprimer.pack(pady=10)


    def inserer_noeud():
        valeur = valeur_insertion.get()  # Récupère la valeur depuis la zone de texte
        if valeur:
            valeur = int(valeur)  # Convertit la valeur en entier
            arbre.inserer(valeur)  # Insère la valeur dans l'arbre binaire
            canvas.delete("all")  # Efface le canevas
            arbre.dessiner(canvas, 400, 30, 200)  # Redessine l'arbre avec la nouvelle configuration
        entry_inserer.pack_forget()  # Cache la zone de texte d'insertion
        btn_inserer.pack_forget()  # Cache le bouton insérer
        valeur_insertion.set('')  # Efface la zone de texte après l'insertion
        hide_widgets()  # Cache les widgets après l'insertion

    def supprimer_noeud():
        valeur = valeur_suppression.get()
        if valeur:
            valeur = int(valeur)
            arbre.supprimer(valeur)
            canvas.delete("all")
            arbre.dessiner(canvas, 400, 30, 200)
        entry_supprimer.pack_forget()  # Cacher la zone de texte
        btn_supprimer.pack_forget()  # Cacher le bouton supprimer
        hide_widgets()  # Cache les widgets après la suppression

    # Création des boutons qui ne sont pas immédiatement affichés
    btn_inserer = ttk.Button(sidebar, text="Insérer", command=inserer_noeud)
    btn_supprimer = ttk.Button(sidebar, text="Supprimer", command=supprimer_noeud)

    def afficher_parcours(mode):
        global is_paused, is_stopped
        is_paused = False
        is_stopped = False
        hide_widgets()
        resultat = []
        espace_initial = 200
        x_initial = 400
        y_initial = 30
        canvas.delete("all")
        arbre.dessiner(canvas, x_initial, y_initial, espace_initial)
        
        # Réinitialiser le label_resultat_parcours avant le parcours
        label_resultat_parcours.pack_forget()
        resultat_parcours.set("")
        
        if mode == "prefixe":
            arbre.parcours_prefixe(arbre.racine, resultat, canvas, x_initial, y_initial, espace_initial)
        elif mode == "infixe":
            arbre.parcours_infixe(arbre.racine, resultat, canvas, x_initial, y_initial, espace_initial)
        elif mode == "postfixe":
            arbre.parcours_postfixe(arbre.racine, resultat, canvas, x_initial, y_initial, espace_initial)
        
        label_resultat_parcours.pack(pady=10, padx=5, fill='x')  # Affiche le label de résultat

        # Mettre à jour le StringVar avec le résultat du parcours
        resultat_parcours.set(', '.join(str(x) for x in resultat))
        # Affichez le label
        label_resultat_parcours.pack(pady=10, padx=5, fill='x')


    ttk.Button(sidebar, text="Insérer un nœud", command=show_entry_inserer).pack(pady=15,padx=40)
    ttk.Button(sidebar, text="Supprimer un nœud", command=show_entry_supprimer).pack(pady=15,padx=40)

    ttk.Button(sidebar, text="Parcours Préfixe", command=lambda: afficher_parcours("prefixe")).pack(pady=15,padx=40)
    ttk.Button(sidebar, text="Parcours Infixe", command=lambda: afficher_parcours("infixe")).pack(pady=15,padx=40)
    ttk.Button(sidebar, text="Parcours Postfixe", command=lambda: afficher_parcours("postfixe")).pack(pady=15,padx=40)
    
    # Créer un frame pour les boutons d'animation en bas
    control_frame = tk.Frame(root, bg='white')
    control_frame.pack(side='bottom', fill='x')  
    
    # Utiliser des caractères Unicode pour les symboles des boutons
    play_symbol = "\u25B6"  # Symbole 'Play'
    pause_symbol = "\u23F8" # Symbole 'Pause'
    stop_symbol = "\u23F9"  # Symbole 'Stop'
    


    # Ajouter des boutons avec des symboles pour contrôler l'animation
    ttk.Button(control_frame, text=play_symbol, command=start_animation).pack(side='left', padx=20)
    ttk.Button(control_frame, text=pause_symbol, command=pause_animation).pack(side='left', padx=20)
    ttk.Button(control_frame, text=stop_symbol, command=stop_animation).pack(side='left', padx=20)


    root.mainloop()

if __name__ == "__main__":
    main()
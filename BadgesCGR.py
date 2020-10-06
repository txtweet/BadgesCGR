# -*- coding : utf8 -*-
# !/usr/bin/env python3
import csv
import os
import tkinter as tk
from time import strftime
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, askokcancel
from tkinter.scrolledtext import ScrolledText
import configparser
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date

# Format table CSV OP_CODE;OP_Descritpion;Identifiant;Numero;Etat;Responsable;Téléhpone;Club;CleCoffre;CleCGR
# ;PorteBadge;Statut;Lieu;Remarque;DatePret;HeurePret;Caution;TypePret;DateRetour;HeureRetour
# OP_Code : 0 : Ajout d'un badge, 1 : Modification d'un badge, 2 : Sortie de badge, 3 : Retour d'un badge,
# 4, Suppresion d'un badge


class Ajout(tk.Toplevel):
    def __init__(self, parent, badges):
        tk.Toplevel.__init__(self, parent)
        self.title("Ajouter un badge")
        self.badges = badges
        self.label = tk.Label(self, text="Modification d'un badge").grid(row=0, column=0, columnspan=4, sticky='N',
                                                                         pady=2)

        self.varId = tk.StringVar()
        self.lab_Id = tk.Label(self, text="Identifiant du badge :").grid(row=1, column=0, sticky='W', pady=2)
        self.ent_Id = tk.Entry(self, textvariable=self.varId, width=30).grid(row=1, column=1,
                                                                             columnspan=3,
                                                                             sticky='N',
                                                                             pady=2)

        self.varNumero = tk.StringVar()
        self.lab_numero = tk.Label(self, text="Numero du badge :").grid(row=2, column=0, sticky='W', pady=2)
        self.ent_numero = tk.Entry(self, textvariable=self.varNumero, width=30).grid(row=2, column=1,
                                                                                     columnspan=3,
                                                                                     sticky='N',
                                                                                     pady=2)

        self.varEtat = tk.StringVar()
        self.lab_etat = tk.Label(self, text="Etat du badge :").grid(row=3, column=0, sticky='W', pady=2)
        self.list_etat = ["Bon", "Moyen", "Mauvais"]
        self.combo_etat = ttk.Combobox(self, values=self.list_etat, textvariable=self.varEtat).grid(row=3,
                                                                                                                column=1,
                                                                                                                columnspan=3,
                                                                                                                sticky='N',
                                                                                                                pady=2)
        self.varEtat.set(self.list_etat[0])
        self.varCoffre = tk.IntVar()
        self.case_Coffre = tk.Checkbutton(self, text="Clé du coffre asso", variable=self.varCoffre).grid(row=12,
                                                                                                         column=0,
                                                                                                         columnspan=4,
                                                                                                         sticky='N',
                                                                                                         pady=2)

        self.varPorteBadge = tk.IntVar()
        self.case_PorteBadge = tk.Checkbutton(self, text="Porte Badge", variable=self.varPorteBadge).grid(row=13,
                                                                                                          column=0,
                                                                                                          columnspan=4,
                                                                                                          sticky='N',
                                                                                                          pady=2)

        self.varCgr = tk.IntVar()
        self.case_Cgr = tk.Checkbutton(self, text="Clé du bureau CGR", variable=self.varCgr).grid(
            row=14,
            column=0,
            columnspan=4,
            sticky='N',
            pady=2)

        self.lab_remarque = tk.Label(self, text="Remarque/Commentaire :").grid(row=16, column=0, sticky='W', pady=2)
        # self.ent_remarque = tk.Entry(self, textvariable=self.varEtat, width=30).grid(row=15, column=1,
        # columnspan=3, sticky='W',pady=2)
        self.ent_remarque = ScrolledText(self, width=30, height=3)
        self.ent_remarque.grid(row=16, column=1, columnspan=3, sticky='W', pady=2)
        self.bouton_valider = tk.Button(self, text="Valider la saisie", command=self.testdonne).grid(row=17, column=0,
                                                                                                     columnspan=2,
                                                                                                     sticky='N', pady=2)

        self.bouton_quitter = tk.Button(self, text="Quitter la saisie", command=self.quitter).grid(row=17, column=2,
                                                                                                   columnspan=2,
                                                                                                   sticky='N', pady=2)
        self.protocol('WM_DELETE_WINDOW', self.quitter)

    def quitter(self):
        quit = askokcancel("Attention", "Voulez-vous quitter sans enregistrer vos modifications ?", parent=self)
        if quit:
            self.destroy()
        else:
            pass

    def testdonne(self):
        error_str = ""
        error = 0

        if len(self.varId.get()) < 1:
            error += 1
            error_str += "L'identifiant du badge ne peut être vide\n"
        if len(self.varNumero.get()) < 1:
            error += 1
            error_str += "Le numero du badge ne peut être vide\n"
        if len(self.varEtat.get()) < 1:
            error += 1
            error_str += "L'état du badge ne peut être vide\n"
        if self.varId.get() in self.badges:
            error += 1
            error_str += "Un badge avec le même identifiant existe déjà\n"

        if (error != 0):
            showerror("Erreur de saisie", error_str, parent=self)
        else:
            self.val()

    def val(self):
        badge = {}
        badge['numero'] = self.varNumero.get()
        badge['etat'] = self.varEtat.get()
        badge['coffre'] = self.varCoffre.get()
        badge['portebadge'] = self.varPorteBadge.get()
        badge['cgr'] = self.varCgr.get()
        badge['remarque'] = self.ent_remarque.get("1.0", tk.END)
        badge['responsable'] = ''
        badge['telephone'] = ''
        badge['club'] = ''
        badge['statut'] = "disponible"
        badge['datepret'] = ''
        badge['heurepret'] = ''
        badge['dateretour'] = ''
        badge['heureretour'] = ''
        badge['caution'] = ''
        badge['type'] = ''
        badge['lieu'] = ''
        self.badges[self.varId.get()] = badge
        log_writer(0, self.varId.get(), badge)
        showinfo("Création du badge effectuée", "Les informations ont bien été prises en compte", parent=self)
        self.destroy()


class Sortie(tk.Toplevel):
    def __init__(self, parent, badge, nom):
        tk.Toplevel.__init__(self, parent)
        self.title("Sortie de Badge")
        self.badge = badge
        self.nom = nom
        # Label constructeur, paramtres du widget
        self.label = tk.Label(self, text="Sortie du badge " + str(nom)).grid(row=0, column=0, columnspan=4, sticky='N',
                                                                             pady=2)

        self.varNumero = tk.StringVar()
        self.varNumero.set(badge['numero'])
        self.lab_numero = tk.Label(self, text="Numero du badge :").grid(row=1, column=0, sticky='W', pady=2)
        self.ent_numero = tk.Entry(self, textvariable=self.varNumero, state='disabled', width=30).grid(row=1, column=1,
                                                                                                       columnspan=3,
                                                                                                       sticky='N',
                                                                                                       pady=2)

        self.varEtat = tk.StringVar()
        self.varEtat.set(badge['etat'])
        self.lab_etat = tk.Label(self, text="Etat du badge :").grid(row=2, column=0, sticky='W', pady=2)
        self.list_etat = ["Bon", "Moyen", "Mauvais"]
        self.combo_etat = ttk.Combobox(self, values=self.list_etat, textvariable=self.varEtat).grid(row=2,
                                                                                                                column=1,
                                                                                                                columnspan=3,
                                                                                                                sticky='N',
                                                                                                                pady=2)
        
        self.varNom = tk.StringVar()
        self.lab_nom = tk.Label(self, text="Nom du responsable :").grid(row=3, column=0, sticky='W', pady=2)
        self.ent_nom = tk.Entry(self, textvariable=self.varNom, width=30).grid(row=3, column=1, columnspan=3,
                                                                               sticky='N', pady=2)

        self.varTel = tk.StringVar()
        self.lab_tel = tk.Label(self, text="Téléphone du responsable :").grid(row=4, column=0, sticky='W', pady=2)
        self.ent_tel = tk.Entry(self, textvariable=self.varTel, width=30).grid(row=4, column=1, columnspan=3,
                                                                               sticky='N', pady=2)

        self.varClub = tk.StringVar()
        self.lab_club = tk.Label(self, text="Asso/Entité :").grid(row=5, column=0, sticky='W', pady=2)
        self.ent_club = tk.Entry(self, textvariable=self.varClub, width=30).grid(row=5, column=1, columnspan=3,
                                                                                 sticky='N', pady=2)

        self.lab_datepret = tk.Label(self, text="Date du prêt :").grid(row=6, column=0, sticky='W', pady=2)
        self.calpret = DateEntry(self, locale='fr_FR', bg="darkblue", fg="white")
        self.calpret.grid(row=6, column=1, columnspan=3, sticky='N', pady=2)
        self.varHhpret = tk.StringVar()
        self.varMmpret = tk.StringVar()
        self.lab_heurepret = tk.Label(self, text="Heure du prêt :").grid(row=7, column=0, sticky='W', pady=2)
        self.ent_hhpret = tk.Entry(self, textvariable=self.varHhpret, width=10).grid(row=7, column=1, sticky='E',
                                                                                     pady=2)
        self.labPheurepret = tk.Label(self, text=" : ").grid(row=7, column=2, sticky='N', pady=2)
        self.ent_mmpret = tk.Entry(self, textvariable=self.varMmpret, width=10).grid(row=7, column=3, sticky='W',
                                                                                     pady=2)
        self.varHhpret.set(datetime.now().hour)
        self.varMmpret.set(datetime.now().minute)

        self.lab_dateret = tk.Label(self, text="Date du retour :").grid(row=8, column=0, sticky='W', pady=2)
        self.calret = tk.Entry(self, textvariable="__/__/____", state='disabled', width=30).grid(row=8, column=1,
                                                                                                 columnspan=3,
                                                                                                 sticky='N', pady=2)
        self.lab_heureret = tk.Label(self, text="Heure du retour :").grid(row=9, column=0, sticky='W', pady=2)
        self.ent_hhret = tk.Entry(self, state='disabled', width=10).grid(row=9, column=1, sticky='E', pady=2)
        self.labPheureret = tk.Label(self, text=" : ").grid(row=9, column=2, sticky='N', pady=2)
        self.ent_mmret = tk.Entry(self, state='disabled', width=10).grid(row=9, column=3, sticky='W', pady=2)

        self.varCaution = tk.IntVar()
        self.lab_caution = tk.Label(self, text="Caution :").grid(row=10, column=0, sticky='W', pady=2)
        self.rb_cautoui = tk.Radiobutton(self, text='Oui', variable=self.varCaution, value=1).grid(row=10, column=1,
                                                                                                   sticky='W', pady=2)
        self.rb_cautnon = tk.Radiobutton(self, text='Non', variable=self.varCaution, value=0).grid(row=10, column=2,
                                                                                                   sticky='W', pady=2)
        self.varCaution.set(0)

        self.varCoffre = tk.IntVar()
        if str(badge['coffre']) == '1':
            self.varCoffre.set(1)
        else:
            self.varCoffre.set(0)
        self.case_Coffre = tk.Checkbutton(self, text="Clé du coffre asso", variable=self.varCoffre).grid(row=11,
                                                                                                         column=0,
                                                                                                         columnspan=4,
                                                                                                         sticky='N',
                                                                                                         pady=2)

        self.varPorteBadge = tk.IntVar()
        if str(badge['portebadge']) == '1':
            self.varPorteBadge.set(1)
        else:
            self.varPorteBadge.set(0)
        self.case_PorteBadge = tk.Checkbutton(self, text="Porte Badge", variable=self.varPorteBadge).grid(row=12,
                                                                                                          column=0,
                                                                                                          columnspan=4,
                                                                                                          sticky='N',
                                                                                                          pady=2)

        self.varCgr = tk.IntVar()
        if str(badge['cgr']) == '1':
            self.varCgr.set(1)
        else:
            self.varCgr.set(0)
        self.case_Cgr = tk.Checkbutton(self, text="Clé du bureau CGR", variable=self.varCgr).grid(row=13,
                                                                                                  column=0,
                                                                                                  columnspan=4,
                                                                                                  sticky='N',
                                                                                                  pady=2)

        self.lab_lieu = tk.Label(self, text="Lieu du badge :").grid(row=14, column=0, sticky='W', pady=2)
        self.ent_lieu = tk.Entry(self, state='disabled', width=30).grid(row=14, column=1, columnspan=3, sticky='N',
                                                                        pady=2)

        self.lab_typepret = tk.Label(self, text="Type de pret :").grid(row=15, column=0, sticky='W', pady=2)
        self.varTypepret = tk.StringVar()
        self.list_typepret = ["Ponctuel", "A l'année"]
        self.combo_typepret = ttk.Combobox(self, values=self.list_typepret, textvariable=self.varTypepret).grid(row=15,
                                                                                                                column=1,
                                                                                                                columnspan=3,
                                                                                                                sticky='N',
                                                                                                                pady=2)
        self.varTypepret.set(self.list_typepret[0])

        self.lab_remarque = tk.Label(self, text="Remarque/Commentaire :").grid(row=16, column=0, sticky='W', pady=2)
        # self.ent_remarque = tk.Entry(self, textvariable=self.varEtat, width=30).grid(row=15, column=1, columnspan=3, sticky='W',pady=2)
        self.ent_remarque = ScrolledText(self, width=30, height=3)
        self.ent_remarque.grid(row=16, column=1, columnspan=3, sticky='W', pady=2)
        self.ent_remarque.insert(tk.INSERT, badge['remarque'])

        self.bouton_valider = tk.Button(self, text="Valider la saisie", command=self.testdonne).grid(row=17, column=0,
                                                                                                     columnspan=2,
                                                                                                     sticky='N', pady=2)

        self.bouton_quitter = tk.Button(self, text="Quitter la saisie", command=self.quitter).grid(row=17, column=2,
                                                                                                   columnspan=2,
                                                                                                   sticky='N', pady=2)
        self.protocol('WM_DELETE_WINDOW', self.quitter)

    def quitter(self):
        quit = askokcancel("Attention", "Voulez-vous quitter sans enregistrer vos modifications ?", parent=self)
        if quit:
            self.destroy()
        else:
            pass

    def testdonne(self):
        error_str = ""
        error = 0
        try:
            int(self.varHhpret.get())
            int(self.varMmpret.get())
            assert 0 <= int(self.varHhpret.get()) < 24
            assert 0 <= int(self.varMmpret.get()) < 60
        except ValueError:

            error += 1
            error_str += "L'heure saisie doit contenir seulement des chiffres\n"
        except AssertionError:

            error += 1
            error_str += "L'heure saisie doit être une heure valide\n"
        else:
            self.datepret = str(self.calpret.get())
            self.heurepret = self.varHhpret.get() + "h" + self.varMmpret.get()
        if len(self.varEtat.get()) < 1:
            error += 1
            error_str += "L'état du badge ne peut être vide\n"
        if len(self.varNom.get()) < 1:
            error += 1
            error_str += "Le nom du responsable ne peut être vide\n"
        if len(self.varTel.get()) < 1:
            error += 1
            error_str += "Le numero du responsable ne peut être vide\n"
        if len(self.varClub.get()) < 1:
            error += 1
            error_str += "L'entité du responsable ne peut être vide\n"
        if len(self.varTypepret.get()) < 1:
            error += 1
            error_str += "Merci de selectionner le type de pret\n"

        if (error != 0):
            showerror("Erreur de saisie", error_str, parent=self)
        else:
            self.val()

    def val(self):
        self.badge['datepret'] = self.datepret
        self.badge['heurepret'] = self.heurepret
        self.badge['etat'] = self.varEtat.get()
        self.badge['responsable'] = self.varNom.get()
        self.badge['telephone'] = self.varTel.get()
        self.badge['club'] = self.varClub.get()
        self.badge['caution'] = self.varCaution.get()
        self.badge['coffre'] = self.varCoffre.get()
        self.badge['portebadge'] = self.varPorteBadge.get()
        self.badge['cgr'] = self.varCgr.get()
        self.badge['type'] = self.varTypepret.get()
        self.badge['lieu'] = ''
        self.badge['dateretour'] = ''
        self.badge['heureretour'] = ''
        self.badge['statut'] = "prete"
        self.badge['remarque'] = self.ent_remarque.get("1.0", tk.END)
        log_writer(2, self.nom, self.badge)
        showinfo("Sortie de badge effectuée", "Les informations ont bien été prises en compte", parent=self)

        self.destroy()


class Retour(tk.Toplevel):
    def __init__(self, parent, badge, nom):
        tk.Toplevel.__init__(self, parent)
        self.title("Retour de Badge")
        self.badge = badge
        self.nom = nom
        # Label constructeur, paramtres du widget
        self.label = tk.Label(self, text="Retour du badge" + str(nom)).grid(row=0, column=0, columnspan=4, sticky='N',
                                                                            pady=2)

        self.varNumero = tk.StringVar()
        self.varNumero.set(badge['numero'])
        self.lab_numero = tk.Label(self, text="Numero du badge :").grid(row=1, column=0, sticky='W', pady=2)
        self.ent_numero = tk.Entry(self, textvariable=self.varNumero, state='disabled', width=30).grid(row=1, column=1,
                                                                                                       columnspan=3,
                                                                                                       sticky='N',
                                                                                                       pady=2)

        self.varEtat = tk.StringVar()
        self.varEtat.set(badge['etat'])
        self.lab_etat = tk.Label(self, text="Etat du badge :").grid(row=2, column=0, sticky='W', pady=2)
        self.list_etat = ["Bon", "Moyen", "Mauvais"]
        self.combo_etat = ttk.Combobox(self, values=self.list_etat, textvariable=self.varEtat, state='disabled').grid(row=2,
                                                                                                                column=1,
                                                                                                                columnspan=3,
                                                                                                                sticky='N',
                                                                                                                pady=2)
        self.varNom = tk.StringVar()
        self.varNom.set(self.badge['responsable'])
        self.lab_nom = tk.Label(self, text="Nom du responsable :").grid(row=3, column=0, sticky='W', pady=2)
        self.ent_nom = tk.Entry(self, textvariable=self.varNom, state='disabled', width=30).grid(row=3, column=1,
                                                                                                 columnspan=3,
                                                                                                 sticky='N', pady=2)

        self.varTel = tk.StringVar()
        self.varTel.set(self.badge['telephone'])
        self.lab_tel = tk.Label(self, text="Téléphone du responsable :").grid(row=4, column=0, sticky='W', pady=2)
        self.ent_tel = tk.Entry(self, textvariable=self.varTel, state='disabled', width=30).grid(row=4, column=1,
                                                                                                 columnspan=3,
                                                                                                 sticky='N', pady=2)

        self.varClub = tk.StringVar()
        self.varClub.set(self.badge['club'])
        self.lab_club = tk.Label(self, text="Asso/Entité :").grid(row=5, column=0, sticky='W', pady=2)
        self.ent_club = tk.Entry(self, textvariable=self.varClub, state='disabled', width=30).grid(row=5, column=1,
                                                                                                   columnspan=3,
                                                                                                   sticky='N', pady=2)

        self.lab_datepret = tk.Label(self, text="Date du prêt :").grid(row=6, column=0, sticky='W', pady=2)
        self.lab_pret = tk.Label(self, text=badge['datepret'])
        self.lab_pret.grid(row=6, column=1, columnspan=3, sticky='N', pady=2)
        self.lab_heurepret = tk.Label(self, text="Heure du prêt :").grid(row=7, column=0, sticky='W', pady=2)
        self.lab_affheurepret = tk.Label(self, text=self.badge['heurepret']).grid(row=7, column=1,
                                                                                  columnspan=3,
                                                                                  sticky='N', pady=2)

        self.lab_dateret = tk.Label(self, text="Date du retour :").grid(row=8, column=0, sticky='W', pady=2)
        self.calret = DateEntry(self, locale='fr_FR', bg="darkblue", fg="white")
        self.calret.grid(row=8, column=1, columnspan=3, sticky='N', pady=2)
        self.varHhret = tk.StringVar()
        self.varMmret = tk.StringVar()
        self.lab_heureret = tk.Label(self, text="Heure du retour :").grid(row=9, column=0, sticky='W', pady=2)
        self.ent_hhret = tk.Entry(self, textvariable=self.varHhret, width=10).grid(row=9, column=1, sticky='E',
                                                                                   pady=2)
        self.labPheureret = tk.Label(self, text=" : ").grid(row=9, column=2, sticky='N', pady=2)
        self.ent_mmret = tk.Entry(self, textvariable=self.varMmret, width=10).grid(row=9, column=3, sticky='W',
                                                                                   pady=2)
        self.varHhret.set(datetime.now().hour)
        self.varMmret.set(datetime.now().minute)

        self.varCaution = tk.IntVar()
        self.lab_caution = tk.Label(self, text="Caution :").grid(row=10, column=0, sticky='W', pady=2)
        self.rb_cautoui = tk.Radiobutton(self, text='Oui', variable=self.varCaution, state='disabled', value=1).grid(
            row=10, column=1,
            sticky='W', pady=2)
        self.rb_cautnon = tk.Radiobutton(self, text='Non', variable=self.varCaution, state='disabled', value=0).grid(
            row=10, column=2,
            sticky='W', pady=2)
        if str(badge['caution']) == '1':
            self.varCaution.set(1)
        else:
            self.varCaution.set(0)

        self.varCoffre = tk.IntVar()
        if str(badge['coffre']) == '1':
            self.varCoffre.set(1)
        else:
            self.varCoffre.set(0)
        self.case_Coffre = tk.Checkbutton(self, text="Clé du coffre asso", state='disabled',
                                          variable=self.varCoffre).grid(row=11,
                                                                        column=0,
                                                                        columnspan=4,
                                                                        sticky='N',
                                                                        pady=2)

        self.varPorteBadge = tk.IntVar()
        if str(badge['portebadge']) == '1':
            self.varPorteBadge.set(1)
        else:
            self.varPorteBadge.set(0)
        self.case_PorteBadge = tk.Checkbutton(self, text="Porte Badge", state='disabled',
                                              variable=self.varPorteBadge).grid(row=12,
                                                                                column=0,
                                                                                columnspan=4,
                                                                                sticky='N',
                                                                                pady=2)

        self.varCgr = tk.IntVar()
        if str(badge['cgr']) == '1':
            self.varCgr.set(1)
        else:
            self.varCgr.set(0)
        self.case_Cgr = tk.Checkbutton(self, text="Clé du bureau CGR", state='disabled', variable=self.varCgr).grid(
            row=13,
            column=0,
            columnspan=4,
            sticky='N',
            pady=2)

        self.varLieu = tk.StringVar()
        self.varLieu.set(self.badge['lieu'])
        self.lab_lieu = tk.Label(self, text="Lieu du badge :").grid(row=14, column=0, sticky='W', pady=2)
        self.ent_lieu = tk.Entry(self, textvariable=self.varLieu, width=30).grid(row=14, column=1,
                                                                                 columnspan=3,
                                                                                 sticky='N',
                                                                                 pady=2)
        self.varLieu.set("Pot à badges")

        self.lab_typepret = tk.Label(self, text="Type de pret :").grid(row=15, column=0, sticky='W', pady=2)
        self.varTypepret = tk.StringVar()
        self.varTypepret.set(self.badge['type'])
        self.list_typepret = ["Ponctuel", "A l'année"]
        self.combo_typepret = ttk.Combobox(self, values=self.list_typepret, state='disabled',
                                           textvariable=self.varTypepret).grid(row=15,
                                                                               column=1,
                                                                               columnspan=3,
                                                                               sticky='N',
                                                                               pady=2)

        self.lab_remarque = tk.Label(self, text="Remarque/Commentaire :").grid(row=16, column=0, sticky='W', pady=2)
        # self.ent_remarque = tk.Entry(self, textvariable=self.varEtat, width=30).grid(row=15, column=1, columnspan=3, sticky='W',pady=2)
        self.ent_remarque = ScrolledText(self, width=30, height=3)
        self.ent_remarque.grid(row=16, column=1, columnspan=3, sticky='W', pady=2)
        self.ent_remarque.insert(tk.INSERT, badge['remarque'])

        self.bouton_valider = tk.Button(self, text="Valider la saisie", command=self.testdonne).grid(row=17, column=0,
                                                                                                     columnspan=2,
                                                                                                     sticky='N', pady=2)

        self.bouton_quitter = tk.Button(self, text="Quitter la saisie", command=self.quitter).grid(row=17, column=2,
                                                                                                   columnspan=2,
                                                                                                   sticky='N', pady=2)
        self.protocol('WM_DELETE_WINDOW', self.quitter)

    def quitter(self):
        quit = askokcancel("Attention", "Voulez-vous quitter sans enregistrer vos modifications ?", parent=self)
        if quit:
            self.destroy()
        else:
            pass

    def testdonne(self):
        error_str = ""
        error = 0
        try:
            int(self.varHhret.get())
            int(self.varMmret.get())
            assert 0 <= int(self.varHhret.get()) < 24
            assert 0 <= int(self.varMmret.get()) < 60
        except ValueError:

            error += 1
            error_str += "L'heure saisie doit contenir seulement des chiffres\n"
        except AssertionError:

            error += 1
            error_str += "L'heure saisie doit être une heure valide\n"
        else:
            self.dateret = str(self.calret.get())
            self.heureret = self.varHhret.get() + "h" + self.varMmret.get()

        if len(self.varLieu.get()) < 1:
            error += 1
            error_str += "Le lieu de rangement du badge ne peut être vide\n"

        if (error != 0):
            showerror("Erreur de saisie", error_str, parent=self)
        else:
            self.val()

    def val(self):
        self.badge['dateretour'] = self.dateret
        self.badge['heureretour'] = self.heureret
        self.badge['statut'] = 'disponible'
        self.badge['lieu'] = self.varLieu.get()
        self.badge['remarque'] = self.ent_remarque.get("1.0", tk.END)
        log_writer(3, self.nom, self.badge)
        showinfo("Retour du badge effectuée", "Les informations ont bien été prises en compte", parent=self)
        self.destroy()


class Modification(tk.Toplevel):
    def __init__(self, parent, badges, nom):
        tk.Toplevel.__init__(self, parent)
        self.title("Création d'un Badge")
        self.badges = badges
        self.nom = nom
        self.badge = badges[nom]
        # Label constructeur, paramtres du widget
        self.label = tk.Label(self, text="Modification d'un badge").grid(row=0, column=0, columnspan=4, sticky='N',
                                                                         pady=2)

        self.varId = tk.StringVar()
        self.lab_Id = tk.Label(self, text="Identifiant du badge :").grid(row=1, column=0, sticky='W', pady=2)
        self.ent_Id = tk.Entry(self, textvariable=self.varId, width=30).grid(row=1, column=1,
                                                                             columnspan=3,
                                                                             sticky='N',
                                                                             pady=2)
        self.varId.set(self.nom)

        self.varNumero = tk.StringVar()
        self.lab_numero = tk.Label(self, text="Numero du badge :").grid(row=2, column=0, sticky='W', pady=2)
        self.ent_numero = tk.Entry(self, textvariable=self.varNumero, width=30).grid(row=2, column=1,
                                                                                     columnspan=3,
                                                                                     sticky='N',
                                                                                     pady=2)
        self.varNumero.set(self.badge['numero'])

        self.varEtat = tk.StringVar()
        self.lab_etat = tk.Label(self, text="Etat du badge :").grid(row=3, column=0, sticky='W', pady=2)
        self.list_etat = ["Bon", "Moyen", "Mauvais"]
        self.combo_etat = ttk.Combobox(self, values=self.list_etat, textvariable=self.varEtat).grid(row=3,
                                                                                                                column=1,
                                                                                                                columnspan=3,
                                                                                                                sticky='N',
                                                                                                                pady=2)
        self.varEtat.set(self.badge['etat'])

        self.varStatut = tk.IntVar()
        self.lab_statut = tk.Label(self, text="Statut :").grid(row=4, column=0, sticky='W', pady=2)
        self.rb_statdispo = tk.Radiobutton(self, text='Disponible', variable=self.varStatut, value=0,
                                           command=self.updatepret).grid(
            row=4, column=1, sticky='W', pady=2)
        self.rb_statpret = tk.Radiobutton(self, text='En pret', variable=self.varStatut, value=1,
                                          command=self.updatepret).grid(
            row=4, column=2,
            sticky='W', pady=2)
        if str(self.badge['statut']) == 'disponible':
            self.varStatut.set(0)
        else:
            self.varStatut.set(1)

        self.varNom = tk.StringVar()
        self.lab_nom = tk.Label(self, text="Nom du responsable :").grid(row=5, column=0, sticky='W', pady=2)
        self.ent_nom = tk.Entry(self, textvariable=self.varNom, state='disabled', width=30)
        self.ent_nom.grid(row=5, column=1, columnspan=3, sticky='N', pady=2)

        self.varTel = tk.StringVar()
        self.lab_tel = tk.Label(self, text="Téléphone du responsable :").grid(row=6, column=0, sticky='W', pady=2)
        self.ent_tel = tk.Entry(self, textvariable=self.varTel, state='disabled', width=30)
        self.ent_tel.grid(row=6, column=1, columnspan=3, sticky='N', pady=2)

        self.varClub = tk.StringVar()
        self.lab_club = tk.Label(self, text="Asso/Entité :").grid(row=7, column=0, sticky='W', pady=2)
        self.ent_club = tk.Entry(self, textvariable=self.varClub, state='disabled', width=30)
        self.ent_club.grid(row=7, column=1, columnspan=3, sticky='N', pady=2)

        self.lab_datepret = tk.Label(self, text="Date du prêt :").grid(row=8, column=0, sticky='W', pady=2)
        self.calpret = DateEntry(self, locale='fr_FR', bg="darkblue", fg="white", state='disabled')
        self.calpret.grid(row=8, column=1, columnspan=3, sticky='N', pady=2)
        self.varHhpret = tk.StringVar()
        self.varMmpret = tk.StringVar()
        self.lab_heurepret = tk.Label(self, text="Heure du prêt :")
        self.lab_heurepret.grid(row=9, column=0, sticky='W', pady=2)
        self.ent_hhpret = tk.Entry(self, textvariable=self.varHhpret, state='disabled', width=10)
        self.ent_hhpret.grid(row=9, column=1, sticky='E', pady=2)
        self.labPheurepret = tk.Label(self, text=" : ").grid(row=9, column=2, sticky='N', pady=2)
        self.ent_mmpret = tk.Entry(self, textvariable=self.varMmpret, state='disabled', width=10)
        self.ent_mmpret.grid(row=9, column=3, sticky='W', pady=2)

        self.varCaution = tk.IntVar()
        self.lab_caution = tk.Label(self, text="Caution :").grid(row=10, column=0, sticky='W', pady=2)
        self.rb_cautoui = tk.Radiobutton(self, text='Oui', variable=self.varCaution, state='disabled', value=1)
        self.rb_cautoui.grid(row=10, column=1, sticky='W', pady=2)
        self.rb_cautnon = tk.Radiobutton(self, text='Non', variable=self.varCaution, state='disabled', value=0)
        self.rb_cautnon.grid(row=10, column=2, sticky='W', pady=2)
        if str(self.badge['caution']) == '1':
            self.varCaution.set(1)
        else:
            self.varCaution.set(0)

        self.lab_typepret = tk.Label(self, text="Type de pret :").grid(row=11, column=0, sticky='W', pady=2)
        self.varTypepret = tk.StringVar()
        self.varTypepret.set('')
        self.list_typepret = ["Ponctuel", "A l'année"]
        self.combo_typepret = ttk.Combobox(self, values=self.list_typepret, state='disabled',
                                           textvariable=self.varTypepret)
        self.combo_typepret.grid(row=11, column=1, columnspan=3, sticky='N', pady=2)

        self.varCoffre = tk.IntVar()
        if str(self.badge['coffre']) == '1':
            self.varCoffre.set(1)
        else:
            self.varCoffre.set(0)
        self.case_Coffre = tk.Checkbutton(self, text="Clé du coffre asso", variable=self.varCoffre).grid(row=12,
                                                                                                         column=0,
                                                                                                         columnspan=4,
                                                                                                         sticky='N',
                                                                                                         pady=2)

        self.varPorteBadge = tk.IntVar()
        if str(self.badge['portebadge']) == '1':
            self.varPorteBadge.set(1)
        else:
            self.varPorteBadge.set(0)
        self.case_PorteBadge = tk.Checkbutton(self, text="Porte Badge", variable=self.varPorteBadge).grid(row=13,
                                                                                                          column=0,
                                                                                                          columnspan=4,
                                                                                                          sticky='N',
                                                                                                          pady=2)

        self.varCgr = tk.IntVar()
        if str(self.badge['cgr']) == '1':
            self.varCgr.set(1)
        else:
            self.varCgr.set(0)
        self.case_Cgr = tk.Checkbutton(self, text="Clé du bureau CGR", variable=self.varCgr).grid(
            row=14,
            column=0,
            columnspan=4,
            sticky='N',
            pady=2)

        self.varLieu = tk.StringVar()
        self.lab_lieu = tk.Label(self, text="Lieu du badge :").grid(row=15, column=0, sticky='W', pady=2)
        self.ent_lieu = tk.Entry(self, textvariable=self.varLieu, width=30)
        self.ent_lieu.grid(row=15, column=1, columnspan=3, sticky='N', pady=2)
        self.varLieu.set(self.badge['lieu'])

        self.lab_remarque = tk.Label(self, text="Remarque/Commentaire :").grid(row=16, column=0, sticky='W', pady=2)
        # self.ent_remarque = tk.Entry(self, textvariable=self.varEtat, width=30).grid(row=15, column=1, columnspan=3, sticky='W',pady=2)
        self.ent_remarque = ScrolledText(self, width=30, height=3)
        self.ent_remarque.grid(row=16, column=1, columnspan=3, sticky='W', pady=2)
        self.ent_remarque.insert(tk.INSERT, self.badge['remarque'])

        self.bouton_valider = tk.Button(self, text="Valider la saisie", command=self.testdonne).grid(row=17, column=0,
                                                                                                     columnspan=2,
                                                                                                     sticky='N', pady=2)

        self.bouton_quitter = tk.Button(self, text="Quitter la saisie", command=self.quitter).grid(row=17, column=2,
                                                                                                   columnspan=2,
                                                                                                   sticky='N', pady=2)
        self.updatepret()
        self.protocol('WM_DELETE_WINDOW', self.quitter)

    def quitter(self):
        quit = askokcancel("Attention", "Voulez-vous quitter sans enregistrer vos modifications ?", parent=self)
        if quit:
            self.destroy()
        else:
            pass

    def updatepret(self):
        if self.varStatut.get() == 0:  # Badge disponible
            self.ent_nom.configure(state='disabled')
            self.ent_tel.configure(state='disabled')
            self.ent_club.configure(state='disabled')
            self.calpret.configure(state='disabled')
            self.ent_hhpret.configure(state='disabled')
            self.ent_mmpret.configure(state='disabled')
            self.rb_cautoui.configure(state='disabled')
            self.rb_cautnon.configure(state='disabled')
            self.varLieu.set(self.badge['lieu'])
            self.ent_lieu.configure(state='normal')
            self.varTypepret.set('')
            self.combo_typepret.configure(state='disabled')
        else:  # Badge en pret
            self.ent_nom.configure(state='normal')
            self.varNom.set(self.badge['responsable'])
            self.ent_tel.configure(state='normal')
            self.varTel.set(self.badge['telephone'])
            self.ent_club.configure(state='normal')
            self.varClub.set(self.badge['club'])
            self.calpret.configure(state='normal')
            if len(self.badge['datepret']) > 1:
                self.calpret.set_date(self.badge['datepret'])
            self.varNom.set(self.badge['responsable'])
            self.ent_hhpret.configure(state='normal')
            self.varHhpret.set(self.badge['heurepret'][0:2])
            self.ent_mmpret.configure(state='normal')
            self.varMmpret.set(self.badge['heurepret'][3:])
            self.rb_cautoui.configure(state='normal')
            self.rb_cautnon.configure(state='normal')
            self.varCaution.set(self.badge['caution'])
            self.varTypepret.set(self.badge['type'])
            self.varLieu.set('')
            self.ent_lieu.configure(state='disabled')
            self.combo_typepret.configure(state='normal')

    def testdonne(self):
        error_str = ""
        error = 0
        if len(self.varId.get()) < 1:
            error += 1
            error_str += "L'identifiant du badge ne peut être vide\n"
        if len(self.varNumero.get()) < 1:
            error += 1
            error_str += "Le numero du badge ne peut être vide\n"
        if len(self.varEtat.get()) < 1:
            error += 1
            error_str += "L'état du badge ne peut être vide\n"

        if self.varStatut.get() == 0:  # Badge disponible
            if len(self.varLieu.get()) < 1:
                error += 1
                error_str += "Le lieu du badge ne peut être vide\n"
        else:
            try:
                int(self.varHhpret.get())
                int(self.varMmpret.get())
                assert 0 <= int(self.varHhpret.get()) < 24
                assert 0 <= int(self.varMmpret.get()) < 60
            except ValueError:
                error += 1
                error_str += "L'heure saisie doit contenir seulement des chiffres\n"
            except AssertionError:
                error += 1
                error_str += "L'heure saisie doit être une heure valide\n"
            else:
                self.datepret = str(self.calpret.get())
                self.heurepret = self.varHhpret.get() + "h" + self.varMmpret.get()
            if len(self.varNom.get()) < 1:
                error += 1
                error_str += "Le nom du responsable ne peut être vide\n"
            if len(self.varTel.get()) < 1:
                error += 1
                error_str += "Le numero du responsable ne peut être vide\n"
            if len(self.varClub.get()) < 1:
                error += 1
                error_str += "L'entité du responsable ne peut être vide\n"
            if len(self.varTypepret.get()) < 1:
                error += 1
                error_str += "Merci de selectionner le type de pret\n"

        if (error != 0):
            showerror("Erreur de saisie", error_str, parent=self)
        else:
            self.val()

    def val(self):

        badge = {}
        badge['numero'] = self.varNumero.get()
        badge['etat'] = self.varEtat.get()
        badge['coffre'] = self.varCoffre.get()
        badge['portebadge'] = self.varPorteBadge.get()
        badge['cgr'] = self.varCgr.get()
        badge['remarque'] = self.ent_remarque.get("1.0", tk.END)

        if self.varStatut.get() == 0:  # Badge disponible
            badge['responsable'] = ''
            badge['telephone'] = ''
            badge['club'] = ''
            badge['statut'] = "disponible"
            badge['datepret'] = ''
            badge['heurepret'] = ''
            badge['dateretour'] = ''
            badge['heureretour'] = ''
            badge['caution'] = ''
            badge['type'] = ''
            badge['lieu'] = self.varLieu.get()
        else:
            badge['responsable'] = self.varNom.get()
            badge['telephone'] = self.varTel.get()
            badge['club'] = self.varClub.get()
            badge['statut'] = "prete"
            badge['datepret'] = self.datepret
            badge['heurepret'] = self.heurepret
            badge['dateretour'] = ''
            badge['heureretour'] = ''
            badge['caution'] = self.varCaution.get()
            badge['type'] = self.varTypepret.get()
            badge['lieu'] = ''
        del self.badges[self.nom]
        self.badges[self.varId.get()] = badge
        log_writer(1, self.varId.get(), badge)
        showinfo("Mise à jour du badge effectuée", "Les informations ont bien été prises en compte", parent=self)
        # print(self.badge)
        self.destroy()


class Afficher(tk.Toplevel):
    def __init__(self, parent, badge):
        tk.Toplevel.__init__(self, parent)
        self.title("Affichage du Badge")
        self.badge = badge
        # Label constructeur, paramtres du widget
        self.label = tk.Label(self, text="Affichage de badge").grid(row=0, column=0, columnspan=4, sticky='N', pady=2)

        self.varNumero = tk.StringVar()
        self.varNumero.set(badge['numero'])
        self.lab_numero = tk.Label(self, text="Numero du badge :").grid(row=1, column=0, sticky='W', pady=2)
        self.ent_numero = tk.Entry(self, textvariable=self.varNumero, state='disabled', width=30).grid(row=1, column=1,
                                                                                                       columnspan=3,
                                                                                                       sticky='N',
                                                                                                       pady=2)

        self.varEtat = tk.StringVar()
        self.varEtat.set(badge['etat'])
        self.lab_etat = tk.Label(self, text="Etat du badge :").grid(row=2, column=0, sticky='W', pady=2)
        self.ent_etat = tk.Entry(self, textvariable=self.varEtat, state='disabled', width=30).grid(row=2, column=1,
                                                                                                   columnspan=3,
                                                                                                   sticky='N', pady=2)

        self.varNom = tk.StringVar()
        self.varNom.set(self.badge['responsable'])
        self.lab_nom = tk.Label(self, text="Nom du responsable :").grid(row=3, column=0, sticky='W', pady=2)
        self.ent_nom = tk.Entry(self, textvariable=self.varNom, state='disabled', width=30).grid(row=3, column=1,
                                                                                                 columnspan=3,
                                                                                                 sticky='N', pady=2)

        self.varTel = tk.StringVar()
        self.varTel.set(self.badge['telephone'])
        self.lab_tel = tk.Label(self, text="Téléphone du responsable :").grid(row=4, column=0, sticky='W', pady=2)
        self.ent_tel = tk.Entry(self, textvariable=self.varTel, state='disabled', width=30).grid(row=4, column=1,
                                                                                                 columnspan=3,
                                                                                                 sticky='N', pady=2)

        self.varClub = tk.StringVar()
        self.varClub.set(self.badge['club'])
        self.lab_club = tk.Label(self, text="Asso/Entité :").grid(row=5, column=0, sticky='W', pady=2)
        self.ent_club = tk.Entry(self, textvariable=self.varClub, state='disabled', width=30).grid(row=5, column=1,
                                                                                                   columnspan=3,
                                                                                                   sticky='N', pady=2)

        self.lab_datepret = tk.Label(self, text="Date du prêt :").grid(row=6, column=0, sticky='W', pady=2)
        if len(self.badge['datepret']) > 0:
            self.lab_pret = tk.Label(self, text=self.badge['datepret'])
        else:
            self.lab_pret = tk.Label(self, text="__/__/____")
        self.lab_pret.grid(row=6, column=1, columnspan=3, sticky='N', pady=2)
        self.lab_heurepret = tk.Label(self, text="Heure du prêt :").grid(row=7, column=0, sticky='W', pady=2)
        if len(self.badge['heurepret']) > 0:
            self.lab_affheurepret = tk.Label(self, text=self.badge['heurepret'])
        else:
            self.lab_affheurepret = tk.Label(self, text="--h--")

        self.lab_affheurepret.grid(row=7, column=1, columnspan=3, sticky='N', pady=2)

        self.lab_dateret = tk.Label(self, text="Date du retour :").grid(row=8, column=0, sticky='W', pady=2)
        if len(badge['dateretour']) > 0:
            self.calret = tk.Label(self, text=badge['dateretour'])
        else:
            self.calret = tk.Label(self, text="__/__/____")
        self.calret.grid(row=8, column=1, columnspan=3, sticky='N', pady=2)
        self.lab_heureret = tk.Label(self, text="Heure du retour :").grid(row=9, column=0, sticky='W', pady=2)
        if len(badge['heureretour']) > 0:
            self.lab_affheurepret = tk.Label(self, text=badge['heureretour'])
        else:
            self.lab_affheurepret = tk.Label(self, text="--h--")
        self.lab_affheurepret.grid(row=9, column=1, columnspan=3, sticky='N', pady=2)

        self.varCaution = tk.IntVar()
        self.lab_caution = tk.Label(self, text="Caution :").grid(row=10, column=0, sticky='W', pady=2)
        self.rb_cautoui = tk.Radiobutton(self, text='Oui', variable=self.varCaution, state='disabled', value=1).grid(
            row=10, column=1,
            sticky='W', pady=2)
        self.rb_cautnon = tk.Radiobutton(self, text='Non', variable=self.varCaution, state='disabled', value=0).grid(
            row=10, column=2,
            sticky='W', pady=2)
        if str(badge['caution']) == '1':
            self.varCaution.set(1)
        else:
            self.varCaution.set(0)

        self.varCoffre = tk.IntVar()
        if str(badge['coffre']) == '1':
            self.varCoffre.set(1)
        else:
            self.varCoffre.set(0)

        self.case_Coffre = tk.Checkbutton(self, text="Clé du coffre asso", state='disabled',
                                          variable=self.varCoffre).grid(row=11,
                                                                        column=0,
                                                                        columnspan=4,
                                                                        sticky='N',
                                                                        pady=2)

        self.varPorteBadge = tk.IntVar()
        if str(badge['portebadge']) == '1':
            self.varPorteBadge.set(1)
        else:
            self.varPorteBadge.set(0)
        self.case_PorteBadge = tk.Checkbutton(self, text="Porte Badge", state='disabled',
                                              variable=self.varPorteBadge).grid(row=12,
                                                                                column=0,
                                                                                columnspan=4,
                                                                                sticky='N',
                                                                                pady=2)

        self.varCgr = tk.IntVar()
        if str(badge['cgr']) == '1':
            self.varCgr.set(1)
        else:
            self.varCgr.set(0)
        self.case_Cgr = tk.Checkbutton(self, text="Clé du bureau CGR", state='disabled', variable=self.varCgr).grid(
            row=13,
            column=0,
            columnspan=4,
            sticky='N',
            pady=2)

        self.varLieu = tk.StringVar()
        self.varLieu.set(self.badge['lieu'])
        self.lab_lieu = tk.Label(self, text="Lieu du badge :").grid(row=14, column=0, sticky='W', pady=2)
        self.ent_lieu = tk.Entry(self, textvariable=self.varLieu, state='disabled', width=30).grid(row=14, column=1,
                                                                                                   columnspan=3,
                                                                                                   sticky='N',
                                                                                                   pady=2)

        self.lab_typepret = tk.Label(self, text="Type de pret :").grid(row=15, column=0, sticky='W', pady=2)
        self.varTypepret = tk.StringVar()
        self.varTypepret.set(self.badge['type'])
        self.list_typepret = ["Ponctuel", "A l'année"]
        self.combo_typepret = ttk.Combobox(self, values=self.list_typepret, state='disabled',
                                           textvariable=self.varTypepret).grid(row=15,
                                                                               column=1,
                                                                               columnspan=3,
                                                                               sticky='N',
                                                                               pady=2)

        self.lab_remarque = tk.Label(self, text="Remarque/Commentaire :").grid(row=16, column=0, sticky='W', pady=2)
        # self.ent_remarque = tk.Entry(self, textvariable=self.varEtat, width=30).grid(row=15, column=1, columnspan=3, sticky='W',pady=2)
        self.ent_remarque = ScrolledText(self, width=30, height=3)
        self.ent_remarque.grid(row=16, column=1, columnspan=3, sticky='W', pady=2)
        self.ent_remarque.insert(tk.INSERT, badge['remarque'])
        self.ent_remarque.configure(state='disabled')

        self.bouton_quitter = tk.Button(self, text="Quitter", command=self.destroy).grid(row=17, column=0,
                                                                                         columnspan=4,
                                                                                         sticky='N', pady=2)


class Principale(tk.Frame):
    def __init__(self, parent, badges):
        self.badges = badges
        tk.Frame.__init__(self, parent)
        self.parent = parent
        parent.title("Badges de la Rotonde")

        self.msg = tk.Label(self,
                            text="Bienvenue sur le système de gestion de badge de la CGR \n v0.16 - Septembre 2020 - Noé Germani")
        self.msg.grid(row=0, column = 0, columnspan =2, sticky='N', padx=10,pady=10)

        self.lst_badge = tk.Listbox(self)
        self.updateliste()

        self.lst_badge.grid(row=1, column = 0, sticky='NE', padx=10,pady=10)
        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        self.scrollbar.grid(row=1, column=1, sticky='wns')
        self.scrollbar.config(command=self.lst_badge.yview)
        self.lst_badge['yscrollcommand']=self.scrollbar.set

        self.btn_aff = tk.Button(self, text="Affichage de badge",width=30, command=self.fen_aff,)
        self.btn_pret = tk.Button(self, text="Pret de badge", width=30, command=self.fen_sort)
        self.btn_retour = tk.Button(self, text="Retour de badge",width=30, command=self.fen_ret)
        self.btn_modification = tk.Button(self, text="Modification d'un badge",width=30, command=self.fen_modif)
        self.btn_ajout = tk.Button(self, text="Ajouter un badge",width=30, command=self.fen_ajout)
        self.btn_suppr = tk.Button(self, text="Supprimer un badge",width=30, command=self.supprbadge)
        self.btn_about = tk.Button(self, text="A propos de cette application",width=30, command=self.fen_about)

        self.btn_aff.grid(row=2, column = 0,columnspan =2, sticky='N', padx=10,pady=10)
        self.btn_pret.grid(row=3, column = 0,columnspan =2, sticky='N', padx=10,pady=5)
        self.btn_retour.grid(row=4, column = 0,columnspan =2, sticky='N', padx=10,pady=5)
        self.btn_modification.grid(row=5, column = 0,columnspan =2, sticky='N', padx=10,pady=5)
        self.btn_ajout.grid(row=6, column = 0,columnspan =2,padx=10,pady=5)
        self.btn_suppr.grid(row=7, column = 0,columnspan =2,padx=10,pady=5)
        self.btn_about.grid(row=8, column = 0,columnspan =2,padx=10,pady=5)

    def fen_aff(self):
        try:
            nom = self.lst_badge.get(self.lst_badge.curselection())
        except tk.TclError:
            showinfo("Erreur", "Vous devez d'abord selectioner un badge")
        else:
            nom = nom.split(" - ")[0]
            new_aff = Afficher(self.parent, self.badges[nom])

    def fen_ajout(self):
        self.new_ajout = Ajout(self.parent, self.badges)
        self.new_ajout.bind("<Destroy>", self.majlisteajout)

    def fen_modif(self):
        try:
            nom = self.lst_badge.get(self.lst_badge.curselection())
        except tk.TclError:
            showinfo("Erreur", "Vous devez d'abord selectioner un badge")
        else:
            nom = nom.split(" - ")[0]
            self.new_modif = Modification(self.parent, self.badges, nom)
            self.new_modif.bind("<Destroy>", self.majlistemodif)

    def fen_sort(self):
        try:
            nom = self.lst_badge.get(self.lst_badge.curselection())
        except tk.TclError:
            showinfo("Erreur", "Vous devez d'abord selectioner un badge")
        else:
            nom = nom.split(" - ")[0]
            if self.badges[nom]['statut']=='disponible':
                self.new_sort = Sortie(self.parent, self.badges[nom], nom)
                self.new_sort.bind("<Destroy>", self.toprintsort)
            else:
                showerror('Action Impossible',"Impossible de preter un badge déjà en pret")

    def fen_ret(self):
        try:
            nom = self.lst_badge.get(self.lst_badge.curselection())
        except tk.TclError:
            showinfo("Erreur", "Vous devez d'abord selectioner un badge")
        else:
            nom = nom.split(" - ")[0]
            if self.badges[nom]['statut']!='disponible':
                self.new_ret = Retour(self.parent, self.badges[nom], nom)
                self.new_ret.bind("<Destroy>", self.toprintret)
            else:
                showerror('Action Impossible',"Impossible de retourner un badge déjà disponible")
           

    def supprbadge(self):
        try:
            nom = self.lst_badge.get(self.lst_badge.curselection())
        except tk.TclError:
            showinfo("Erreur", "Vous devez d'abord selectioner un badge")
        else:
            nom = nom.split(" - ")[0]
            if askokcancel("Attention", "Etes-vous sûr de vouoloir supprimer le badge " + nom + " ?"):
                log_writer(4, nom, self.badges[nom])
                del self.badges[nom]
            self.updateliste()

    def fen_about(self):
        strabout = "Cette application a été crée pour gerer les badges de la Rotonde.\n Toutes les actions effectuées dans " \
                   "ceete application sont loggée dans le fichier logbadges.csv\n Ce fihcier peut être ouvert avec Calc ou " \
                   "Excel (encodage UTF-8, séparateur ; )\n \n La base de donnée de l'application est contenue dans " \
                   "le fichier badges.ini \n Ce fichier ne doit JAMAIS être modifié manuellement\n" \
                   "Supprimer le fichier badges.ini permet de reinitialiser l'application"

        showinfo("A propos", strabout)

    def majlisteajout(self, e):
        if e.widget is self.new_ajout:
            self.updateliste()

    def majlistemodif(self, e):
        if e.widget is self.new_modif:
            self.updateliste()

    def toprintsort(self, e):
        if e.widget is self.new_sort:
            self.updateliste()

    def toprintret(self, e):
        if e.widget is self.new_ret:
            self.updateliste()

    def updateliste(self):
        self.lst_badge.delete(0, 'end')
        liste =[]
        for key in self.badges:
            if self.badges[key]['statut'] == 'disponible':
                etat = " - Disponible"
            else:
                etat = " - En Prêt"
            liste.append(key + etat)

        liste.sort()
        for i in liste:
            self.lst_badge.insert('end',i)


def import_badges(config):
    liste_badges = {}
    for key in config.sections():
        badge = {}
        for cle, val in config.items(key):
            badge[cle] = val
        liste_badges[key] = badge
    return liste_badges


def export_badges(config, liste_badges):
    for key in config.sections():
        config.remove_section(key)
    for key in liste_badges:
        config.add_section(key)
        config[key] = liste_badges[key]
    val = 0
    while (val == 0):
        try:
            with open("badges.ini", 'w') as configfile:
                config.write(configfile)
        except EnvironmentError:
            showerror("Erreur", "Les modifications n'ont pu être enregistré, la base de donnée est inacessible\n "
                                "Verifiez que le fichiers badges.ini est accessible en écriture")
        else:
            val = 1


def log_writer(code, nom, badge):
    csv.register_dialect('logbadge', delimiter=';', quoting=csv.QUOTE_MINIMAL)
    opcode = ["Ajout", "Modification", "Sortie", "Retour", "Suppresion"]
    datelog = date.today().isoformat()
    heure = datetime.now().strftime("%H:%M:%S")
    csvline = [code, datelog, heure, opcode[code], nom, badge['numero'], badge['etat'], badge['responsable'], badge['telephone'],
               badge['club'], badge['coffre'], badge['cgr'], badge['portebadge'], badge['statut'], badge['lieu'],
               badge['remarque'], badge['datepret'], badge['heurepret'], badge['caution'], badge['type'],
               badge['dateretour'], badge['heureretour']]
    try:
        with open('logbadges.csv'):
            pass
    except IOError:
        try:
            with open('logbadges.csv', 'w', newline='', encoding='utf-8') as logfile:
                csvnomcol = ["OP_CODE","Date","Heure", "OP_Descritpion", "Identifiant", "Numero", "Etat", "Responsable", "Téléhpone",
                             "Club", "CleCoffre", "CleCGR", "PorteBadge", "Statut", "Lieu", "Remarque", "DatePret",
                             "HeurePret", "Caution", "TypePret", "DateRetour", "HeureRetour"]
                writer = csv.writer(logfile, 'logbadge')
                writer.writerow(csvnomcol)
                showinfo("Information", "Aucun fichier de log existant trouvé\n Un nouveau fichier a été crée")
        except EnvironmentError:
            showerror("Erreur", "Impossible de creer le fichier de log logbadges.csv")
    try:
        with open('logbadges.csv', 'a', newline='', encoding='utf-8') as logfile:
            writer = csv.writer(logfile, 'logbadge')
            writer.writerow(csvline)
    except EnvironmentError:
        showerror("Erreur", "Impossible d'inscrire la modification au fichier de log")


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("badges.ini")
    mes_badges = import_badges(config)
    fenetre_princ = tk.Tk()
    if os.name == 'nt':
        fenetre_princ.iconbitmap('cgr.ico')
    else:
        fenetre_princ.iconbitmap('@cgr.xbm')
    Principale(fenetre_princ, mes_badges).pack(side="top", fill="both", expand=True)
    fenetre_princ.mainloop()
    export_badges(config, mes_badges)

def global_menu_links(request):
    return {
        "menu_links": [
            ("Strona główna", "index"),
            ("Mycie paneli", "mycie-paneli"),
            ("Mycie okien", "mycie-okien"),
            ("Koszenie trawników", "koszenie-trawnikow"),
            ("Usługi wysokościowe", "uslugi-wysokosciowe"),
            ("Zabezpieczenia przeciwko ptakom", "zabezpieczenia-przeciwko-ptakom"),
            ("Blog", "blog"),
            ("Kontakt", "kontakt"),
        ]
    }
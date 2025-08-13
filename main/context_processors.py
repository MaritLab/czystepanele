def global_menu_links(request):
    return {
        "menu_links": [
            ("Strona główna", "index"),
            ("Mycie okien", "mycie-okien"), 
            ("Usługi wysokościowe", "uslugi-wysokosciowe"),
            ("Koszenie trawników", "koszenie-trawnikow"),
            ("Mycie paneli", "mycie-paneli"),
            ("Odśnieżanie", "odsniezanie"),
            ("Zabezpieczenia przed ptakami", "zabezpieczenia-przed-ptakami"),
            ("Realizacje", "realizacje"),
            ("Blog", "blog"),
            ("Kontakt", "kontakt"),
        ]
    }
def global_menu_links(request):
    return {
        "menu_links": [
            ("Strona główna", "index"),
            ("Mycie paneli", "mycie-paneli"),
            ("Mycie okien", "mycie-okien"),
            ("Koszenie trawników", "koszenie-trawnikow"),
            ("Usługi wysokościowe", "uslugi-wysokosciowe"),
            ("Zabezpieczenia przed ptakami", "zabezpieczenia-przed-ptakami"),
            ("Realizacje", "realizacje"),
            ("Blog", "blog"),
            ("Kontakt", "kontakt"),
        ]
    }
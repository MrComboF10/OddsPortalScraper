import oddsportal

odds_portal = oddsportal.OddsPortal()

odds_portal.load_file()

odds_portal.scrap_seasons()

odds_portal.create_wb()

odds_portal.close()

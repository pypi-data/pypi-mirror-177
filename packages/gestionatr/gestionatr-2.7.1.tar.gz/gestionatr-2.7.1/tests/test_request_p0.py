from gestionatr.cli import request_p0
def aux():
    def purge_crm_lead(c, cups):
        #import pudb;pu.db
        cups = cups[:20]
        lead_ids = c.GiscedataCrmLead.search([('cups', 'like', cups)])
        if not lead_ids:
            return False, "Sin leads"
        c.GiscedataCrmLead.write(lead_ids, {'state': 'cancel'})
        polissa_ids = [x['polissa_id'][0] for x in c.GiscedataCrmLead.read(lead_ids, ['polissa_id']) if x['polissa_id']]
        if not polissa_ids:
            return True
        can_deactivate_cups = True
        for pid in polissa_ids:
            sw_ids = c.GiscedataSwitching.search([('cups_polissa_id', '=', pid)])
            if sw_ids:
                for sw in c.GiscedataSwitching.browse(sw_ids):
                    if sw.step_id.name == "01" and sw.enviament_pendent:
                        sw.write({'state': 'cancel'})
                        c.GiscedataPolissa.write(pid, {'state': 'cancelada'})
                    elif sw.step_id.name == "02" and sw.rebuig:
                        sw.write({'state': 'cancel'})
                        c.GiscedataPolissa.write(pid, {'state': 'cancelada'})
                    else:
                        can_deactivate_cups = False
        if can_deactivate_cups:
            cups_ids = c.GiscedataCupsPs.search([('name', 'like', cups)])
            if cups_ids:
                c.GiscedataCupsPs.write(cups_ids, {'active': False})
        return True


    P0_DEMO = {
        # Funcionen
        # "Iberdrola": {
        #     'url': "https://www.i-de.es/cnmcws/agentes/sync?wsdl",
        #     'user': "EC980Y4",
        #     'password': "9UWyvGv39D",
        #     'cups': "ES0021000008103774WC0F",
        #     'emisora': "0373",
        #     'destino': "0021",
        # },
        # "Iberdrola Gaba": {
        #     'url': "https://www.i-de.es/cnmcws/agentes/sync",
        #     'user': "EC9800N",
        #     'password': "^LZg$9J0[T",
        #     'cups': "ES0021000007770630PP",
        #     'emisora': "1664",
        #     'destino': "0021",
        # },
        # "Morella": {
        #     'url': "https://ov.maestrazgodistribucion.es/Sync?WSDL",
        #     'user': "0373",
        #     'password': "0373_aeQuee3F",
        #     'cups': "ES0189000038091476YE0F",
        #     'emisora': "0373",
        #     'destino': "0189",
        # },
        # "Endesa": {
        #     'url': "http://trader-eapi.de-c1.eu1.cloudhub.io/api/P0?wsdl",
        #     'user': "ea1f02cb9ed04a1da80496255df63870",
        #     'password': "78415Cd1a3e44798A87d642EF0171517",
        #     'cups': "ES0031300002599001TX0F",
        #     'emisora': "0706",
        #     'destino': "0031",
        # },
        # "Fenosa": {
        #     'url': "https://sctd.gasnaturalfenosa.com/sctd/ws/Sync?wsdl",
        #     'user': "1664WSSAP",
        #     'password': "2022Mayo",
        #     'cups': "ES0022000006704409RB1P",
        #     'emisora': "1664",
        #     'destino': "0022",
        # },
        # "Viesgo": {
        #     'url': "https://viesgop0.app.viesgo.com/syncRequest.wsdl",
        #     'user': "0706",
        #     'password': "ENE190#06",
        #     'cups': "ES0027700037401002ZB0F",
        #     'emisora': "0706",
        #     'destino': "0282",
        # },
        # "ELECTRICA DE LA SERRANIA DE RONDA, S.L": {
        #     'url': "https://intercambioxml.electricaserraniaderonda.com/Sync/Sync.svc",
        #     'user': "0971",
        #     'password': "ef8d6c83-7",
        #     'cups': "ES0225000050200275EL0F",
        #     'emisora': "0971",
        #     'destino': "0225",
        # },
        "Agri distri": {
            'url': "https://clients.agrienergiaelectrica.com/Sync?WSDL",
            'user': "0108",
            'password': "aks!AP2dmmm9",
            'cups': "ES0112000000015671QS0F",
            'emisora': "0108",
            'destino': "0112",
        },
        # # No funcionen encara
        # "Dielsur": {
        #     'url': "http://wsp0dielesur.portalswitching.com/WSCurvas.asmx?wsdl",
        #     'user': "1440",
        #     'password': "Test1440",
        #     'cups': "ES0143000000203855EW0F",
        #     'emisora': "1440",
        #     'destino': "0143",
        # },
        # "CIDE": {
        #     'url': "https://switchingsync.sercide.com/BasicSYNCService.svc",
        #     'user': "0370_i1C6N",
        #     'password': "=mYow<umQV`aq",
        #     'cups': "ES0614000000000035ZJ0F",
        #     'emisora': "0706",view_importacio_linia_general_tree
        #     'destino': "0614",
        # },
    }

    import sys
    for distri in P0_DEMO:
        sys.stdout.write(("Testing {}...".format(distri)))
        res = request_p0(url=P0_DEMO[distri]["url"], user=P0_DEMO[distri]["user"], password=P0_DEMO[distri]["password"], params=P0_DEMO[distri])
        if "CodigoDePaso>02" not in res:
            print "ERROR"
        else:
            print "OK"

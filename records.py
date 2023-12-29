import csv
import tic_tac_toe_logic as g


class Stats:
    def __init__(self, file, header):
        self.file = file
        self.header = header
        self.rec_list = []
        self.rec_dict = []

    def update_records(self):
        self.rec_list.clear()
        self.rec_dict.clear()
        with open(self.file, 'r') as fr:
            fr.readline()
            records = list(fr)
            for line in records:
                rec = line.strip('\n')
                rec = rec.split(',')
                self.rec_list.append(rec)

        self.clean_data()
        for pl in g.game.players:
            self.loc_upd_rec(pl)

        r_list = sorted(self.rec_list)

        for r in r_list:
            rd = dict(zip(self.header, r))
            self.rec_dict.append(rd)

        with open(self.file, 'w', newline='\n') as fw:
            writer = csv.DictWriter(fw, fieldnames=self.header)
            writer.writeheader()
            for r in self.rec_dict:
                writer.writerow(r)
        self.rec_list.clear()

    def loc_upd_rec(self, rec):
        found = False
        ind = 0
        if len(self.rec_list) > 0:
            for r in self.rec_list:
                if rec.name == r[0]:
                    if rec.opponent == self.rec_list[ind][4]:
                        self.rec_list[ind][rec.result] += 1
                        found = True
                ind += 1
        if found is False:
            self.rec_list.append([rec.name, 0, 0, 0, rec.opponent])
            self.loc_upd_rec(rec)

    def clean_data(self):
        for i in range(len(self.rec_list)):
            for x in range(1, 4):
                self.rec_list[i][x] = int(self.rec_list[i][x])

    def retrieve_stats(self):
        with open(self.file, 'r') as fr:
            fr.readline()
            records = list(fr)
            for line in records:
                rec = line.strip('\n')
                rec = rec.split(',')
                self.rec_list.append(rec)
            self.clean_data()

    def download_stats(self, pl):
        self.retrieve_stats()
        for p in self.rec_list:
            if p[0] == pl.name:
                for r in range(3):
                    pl.stats['Overall'][r] += p[r +1]
                    if p[4] in pl.stats:
                        pl.stats[p[4]][r] += p[r + 1]
                    else:
                        pl.stats[p[4]] = [0, 0, 0]
                        pl.stats[p[4]][r] = p[r + 1]
        self.rec_list.clear()


playerStats = Stats('records.csv', ['name', 'wins', 'losses', 'ties', 'opponent'])

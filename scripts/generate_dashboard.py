#!/usr/bin/env python3
"""Generate HTML dashboard for 华电科工 (601226) with K-line and volume charts."""

import json
import csv
import os

# === Tushare daily OHLC data (from mcp__tushareMcp__daily) ===
tushare_data = [{"ts_code":"601226.SH","trade_date":"20250701","open":6.08,"high":6.12,"low":6.06,"close":6.12,"pre_close":6.1,"change":0.02,"pct_chg":0.3279,"vol":60196.0,"amount":36632.806},{"ts_code":"601226.SH","trade_date":"20250702","open":6.25,"high":6.49,"low":6.19,"close":6.41,"pre_close":6.12,"change":0.29,"pct_chg":4.7386,"vol":394073.29,"amount":250976.754},{"ts_code":"601226.SH","trade_date":"20250703","open":6.36,"high":6.36,"low":6.25,"close":6.28,"pre_close":6.41,"change":-0.13,"pct_chg":-2.0281,"vol":180960.0,"amount":113778.535},{"ts_code":"601226.SH","trade_date":"20250704","open":6.31,"high":6.41,"low":6.25,"close":6.28,"pre_close":6.28,"change":0.0,"pct_chg":0.0,"vol":132009.76,"amount":83377.498},{"ts_code":"601226.SH","trade_date":"20250707","open":6.4,"high":6.43,"low":6.26,"close":6.35,"pre_close":6.25,"change":0.1,"pct_chg":1.6,"vol":123962.5,"amount":78348.951},{"ts_code":"601226.SH","trade_date":"20250708","open":6.98,"high":6.98,"low":6.54,"close":6.6,"pre_close":6.35,"change":0.25,"pct_chg":3.937,"vol":450410.07,"amount":300903.763},{"ts_code":"601226.SH","trade_date":"20250709","open":6.46,"high":6.73,"low":6.46,"close":6.54,"pre_close":6.6,"change":-0.06,"pct_chg":-0.9091,"vol":313592.0,"amount":206296.095},{"ts_code":"601226.SH","trade_date":"20250710","open":6.5,"high":7.05,"low":6.5,"close":6.77,"pre_close":6.54,"change":0.23,"pct_chg":3.5168,"vol":379274.3,"amount":257574.443},{"ts_code":"601226.SH","trade_date":"20250711","open":6.78,"high":6.89,"low":6.59,"close":6.64,"pre_close":6.77,"change":-0.13,"pct_chg":-1.9202,"vol":235285.18,"amount":156357.544},{"ts_code":"601226.SH","trade_date":"20250714","open":6.65,"high":6.68,"low":6.6,"close":6.63,"pre_close":6.64,"change":-0.01,"pct_chg":-0.1506,"vol":120156.0,"amount":79738.447},{"ts_code":"601226.SH","trade_date":"20250715","open":6.63,"high":6.66,"low":6.43,"close":6.47,"pre_close":6.63,"change":-0.16,"pct_chg":-2.4133,"vol":182811.49,"amount":118601.583},{"ts_code":"601226.SH","trade_date":"20250716","open":6.43,"high":6.49,"low":6.38,"close":6.4,"pre_close":6.47,"change":-0.07,"pct_chg":-1.0819,"vol":115330.0,"amount":74109.78},{"ts_code":"601226.SH","trade_date":"20250717","open":6.42,"high":6.45,"low":6.37,"close":6.4,"pre_close":6.4,"change":0.0,"pct_chg":0.0,"vol":91069.0,"amount":58316.217},{"ts_code":"601226.SH","trade_date":"20250718","open":6.4,"high":6.45,"low":6.38,"close":6.45,"pre_close":6.4,"change":0.05,"pct_chg":0.7813,"vol":87675.0,"amount":56258.787},{"ts_code":"601226.SH","trade_date":"20250721","open":6.59,"high":6.78,"low":6.55,"close":6.72,"pre_close":6.45,"change":0.27,"pct_chg":4.186,"vol":277721.03,"amount":184747.091},{"ts_code":"601226.SH","trade_date":"20250722","open":6.75,"high":6.82,"low":6.64,"close":6.81,"pre_close":6.72,"change":0.09,"pct_chg":1.3393,"vol":248849.0,"amount":167979.231},{"ts_code":"601226.SH","trade_date":"20250723","open":6.84,"high":6.89,"low":6.67,"close":6.69,"pre_close":6.81,"change":-0.12,"pct_chg":-1.7621,"vol":237609.72,"amount":160785.035},{"ts_code":"601226.SH","trade_date":"20250724","open":6.65,"high":6.75,"low":6.62,"close":6.7,"pre_close":6.69,"change":0.01,"pct_chg":0.1495,"vol":149644.0,"amount":100232.402},{"ts_code":"601226.SH","trade_date":"20250725","open":6.7,"high":6.71,"low":6.6,"close":6.61,"pre_close":6.7,"change":-0.09,"pct_chg":-1.3433,"vol":126491.97,"amount":83942.707},{"ts_code":"601226.SH","trade_date":"20250728","open":6.59,"high":6.62,"low":6.55,"close":6.6,"pre_close":6.61,"change":-0.01,"pct_chg":-0.1513,"vol":75387.32,"amount":49734.702},{"ts_code":"601226.SH","trade_date":"20250729","open":6.6,"high":6.61,"low":6.49,"close":6.58,"pre_close":6.6,"change":-0.02,"pct_chg":-0.303,"vol":89254.5,"amount":58354.717},{"ts_code":"601226.SH","trade_date":"20250730","open":6.54,"high":6.6,"low":6.49,"close":6.52,"pre_close":6.58,"change":-0.06,"pct_chg":-0.9119,"vol":76409.0,"amount":49982.388},{"ts_code":"601226.SH","trade_date":"20250731","open":6.51,"high":6.53,"low":6.42,"close":6.44,"pre_close":6.52,"change":-0.08,"pct_chg":-1.227,"vol":90283.0,"amount":58320.391},{"ts_code":"601226.SH","trade_date":"20250801","open":6.43,"high":6.47,"low":6.42,"close":6.44,"pre_close":6.44,"change":0.0,"pct_chg":0.0,"vol":72276.7,"amount":46595.464},{"ts_code":"601226.SH","trade_date":"20250804","open":6.43,"high":6.49,"low":6.36,"close":6.49,"pre_close":6.44,"change":0.05,"pct_chg":0.7764,"vol":62547.5,"amount":40334.601},{"ts_code":"601226.SH","trade_date":"20250805","open":6.49,"high":6.54,"low":6.48,"close":6.54,"pre_close":6.49,"change":0.05,"pct_chg":0.7704,"vol":61788.0,"amount":40302.21},{"ts_code":"601226.SH","trade_date":"20250806","open":6.54,"high":6.6,"low":6.52,"close":6.58,"pre_close":6.54,"change":0.04,"pct_chg":0.6116,"vol":79643.0,"amount":52331.72},{"ts_code":"601226.SH","trade_date":"20250807","open":6.58,"high":6.59,"low":6.51,"close":6.55,"pre_close":6.58,"change":-0.03,"pct_chg":-0.4559,"vol":56822.0,"amount":37159.768},{"ts_code":"601226.SH","trade_date":"20250808","open":6.58,"high":6.63,"low":6.53,"close":6.61,"pre_close":6.55,"change":0.06,"pct_chg":0.916,"vol":90443.12,"amount":59719.985},{"ts_code":"601226.SH","trade_date":"20250811","open":6.68,"high":6.68,"low":6.6,"close":6.66,"pre_close":6.61,"change":0.05,"pct_chg":0.7564,"vol":105902.02,"amount":70394.244},{"ts_code":"601226.SH","trade_date":"20250812","open":6.66,"high":6.7,"low":6.63,"close":6.67,"pre_close":6.66,"change":0.01,"pct_chg":0.1502,"vol":84296.2,"amount":56215.346},{"ts_code":"601226.SH","trade_date":"20250813","open":6.7,"high":6.85,"low":6.63,"close":6.79,"pre_close":6.67,"change":0.12,"pct_chg":1.7991,"vol":182890.0,"amount":123353.505},{"ts_code":"601226.SH","trade_date":"20250814","open":6.84,"high":6.95,"low":6.72,"close":6.72,"pre_close":6.79,"change":-0.07,"pct_chg":-1.0309,"vol":188409.62,"amount":128631.42},{"ts_code":"601226.SH","trade_date":"20250815","open":6.7,"high":6.82,"low":6.69,"close":6.77,"pre_close":6.72,"change":0.05,"pct_chg":0.744,"vol":133660.28,"amount":90243.529},{"ts_code":"601226.SH","trade_date":"20250818","open":6.85,"high":6.87,"low":6.75,"close":6.77,"pre_close":6.77,"change":0.0,"pct_chg":0.0,"vol":131778.0,"amount":89355.936},{"ts_code":"601226.SH","trade_date":"20250819","open":6.8,"high":6.81,"low":6.74,"close":6.75,"pre_close":6.77,"change":-0.02,"pct_chg":-0.2954,"vol":105483.0,"amount":71406.322},{"ts_code":"601226.SH","trade_date":"20250820","open":6.74,"high":6.78,"low":6.7,"close":6.78,"pre_close":6.75,"change":0.03,"pct_chg":0.4444,"vol":88614.0,"amount":59814.049},{"ts_code":"601226.SH","trade_date":"20250821","open":6.81,"high":6.81,"low":6.73,"close":6.76,"pre_close":6.78,"change":-0.02,"pct_chg":-0.295,"vol":93012.13,"amount":62962.292},{"ts_code":"601226.SH","trade_date":"20250822","open":6.76,"high":6.81,"low":6.72,"close":6.8,"pre_close":6.76,"change":0.04,"pct_chg":0.5917,"vol":101256.83,"amount":68433.32},{"ts_code":"601226.SH","trade_date":"20250825","open":6.98,"high":7.09,"low":6.9,"close":7.01,"pre_close":6.8,"change":0.21,"pct_chg":3.0882,"vol":352144.62,"amount":246546.823},{"ts_code":"601226.SH","trade_date":"20250826","open":7.0,"high":7.04,"low":6.92,"close":6.96,"pre_close":7.01,"change":-0.05,"pct_chg":-0.7133,"vol":182300.0,"amount":127013.526},{"ts_code":"601226.SH","trade_date":"20250827","open":6.96,"high":6.98,"low":6.75,"close":6.76,"pre_close":6.96,"change":-0.2,"pct_chg":-2.8736,"vol":193287.95,"amount":133197.417},{"ts_code":"601226.SH","trade_date":"20250828","open":6.76,"high":6.85,"low":6.55,"close":6.79,"pre_close":6.76,"change":0.03,"pct_chg":0.4438,"vol":181858.99,"amount":122247.972},{"ts_code":"601226.SH","trade_date":"20250829","open":6.8,"high":6.91,"low":6.76,"close":6.9,"pre_close":6.79,"change":0.11,"pct_chg":1.62,"vol":166167.21,"amount":113985.362},{"ts_code":"601226.SH","trade_date":"20250901","open":6.89,"high":6.89,"low":6.77,"close":6.81,"pre_close":6.9,"change":-0.09,"pct_chg":-1.3043,"vol":127658.0,"amount":87102.502},{"ts_code":"601226.SH","trade_date":"20250902","open":6.8,"high":7.06,"low":6.63,"close":6.94,"pre_close":6.81,"change":0.13,"pct_chg":1.909,"vol":256617.9,"amount":175724.474},{"ts_code":"601226.SH","trade_date":"20250903","open":6.99,"high":7.63,"low":6.95,"close":7.27,"pre_close":6.94,"change":0.33,"pct_chg":4.755,"vol":767312.17,"amount":568111.775},{"ts_code":"601226.SH","trade_date":"20250904","open":7.07,"high":7.26,"low":6.89,"close":7.12,"pre_close":7.27,"change":-0.15,"pct_chg":-2.0633,"vol":560510.7,"amount":397519.096},{"ts_code":"601226.SH","trade_date":"20250905","open":7.02,"high":7.27,"low":6.93,"close":7.27,"pre_close":7.12,"change":0.15,"pct_chg":2.1067,"vol":423856.3,"amount":303379.435},{"ts_code":"601226.SH","trade_date":"20250908","open":7.23,"high":7.78,"low":7.18,"close":7.68,"pre_close":7.27,"change":0.41,"pct_chg":5.6396,"vol":622807.92,"amount":465258.826},{"ts_code":"601226.SH","trade_date":"20250909","open":7.55,"high":7.69,"low":7.38,"close":7.66,"pre_close":7.68,"change":-0.02,"pct_chg":-0.2604,"vol":440592.98,"amount":330132.958},{"ts_code":"601226.SH","trade_date":"20250910","open":7.53,"high":7.59,"low":7.34,"close":7.38,"pre_close":7.66,"change":-0.28,"pct_chg":-3.6554,"vol":312129.95,"amount":231811.973},{"ts_code":"601226.SH","trade_date":"20250911","open":7.45,"high":7.46,"low":7.26,"close":7.38,"pre_close":7.38,"change":0.0,"pct_chg":0.0,"vol":254007.27,"amount":186892.124},{"ts_code":"601226.SH","trade_date":"20250912","open":7.34,"high":7.36,"low":7.18,"close":7.26,"pre_close":7.38,"change":-0.12,"pct_chg":-1.626,"vol":280854.64,"amount":203884.453},{"ts_code":"601226.SH","trade_date":"20250915","open":7.23,"high":7.36,"low":7.2,"close":7.3,"pre_close":7.26,"change":0.04,"pct_chg":0.551,"vol":144291.0,"amount":104896.558},{"ts_code":"601226.SH","trade_date":"20250916","open":7.24,"high":7.29,"low":7.11,"close":7.15,"pre_close":7.3,"change":-0.15,"pct_chg":-2.0548,"vol":184137.0,"amount":131879.785},{"ts_code":"601226.SH","trade_date":"20250917","open":7.18,"high":7.25,"low":7.13,"close":7.22,"pre_close":7.15,"change":0.07,"pct_chg":0.979,"vol":115172.82,"amount":82850.503},{"ts_code":"601226.SH","trade_date":"20250918","open":7.21,"high":7.32,"low":6.92,"close":7.03,"pre_close":7.22,"change":-0.19,"pct_chg":-2.6316,"vol":228095.67,"amount":162599.114},{"ts_code":"601226.SH","trade_date":"20250919","open":7.01,"high":7.07,"low":6.91,"close":6.94,"pre_close":7.03,"change":-0.09,"pct_chg":-1.2802,"vol":133909.01,"amount":93355.848},{"ts_code":"601226.SH","trade_date":"20250922","open":6.95,"high":6.96,"low":6.84,"close":6.93,"pre_close":6.94,"change":-0.01,"pct_chg":-0.1441,"vol":87062.0,"amount":59938.521},{"ts_code":"601226.SH","trade_date":"20250923","open":6.93,"high":6.96,"low":6.67,"close":6.86,"pre_close":6.93,"change":-0.07,"pct_chg":-1.0101,"vol":133928.0,"amount":90856.054},{"ts_code":"601226.SH","trade_date":"20250924","open":6.84,"high":6.91,"low":6.78,"close":6.91,"pre_close":6.86,"change":0.05,"pct_chg":0.7289,"vol":80083.7,"amount":54904.376},{"ts_code":"601226.SH","trade_date":"20250925","open":6.9,"high":6.96,"low":6.83,"close":6.83,"pre_close":6.91,"change":-0.08,"pct_chg":-1.1577,"vol":94799.5,"amount":65243.053},{"ts_code":"601226.SH","trade_date":"20250926","open":6.77,"high":7.04,"low":6.75,"close":6.94,"pre_close":6.83,"change":0.11,"pct_chg":1.6105,"vol":134045.5,"amount":93404.428},{"ts_code":"601226.SH","trade_date":"20250929","open":7.03,"high":7.44,"low":6.99,"close":7.23,"pre_close":6.94,"change":0.29,"pct_chg":4.1787,"vol":250189.32,"amount":180293.003},{"ts_code":"601226.SH","trade_date":"20250930","open":7.23,"high":7.25,"low":7.07,"close":7.18,"pre_close":7.23,"change":-0.05,"pct_chg":-0.6916,"vol":156893.88,"amount":112535.004},{"ts_code":"601226.SH","trade_date":"20251009","open":7.14,"high":7.26,"low":7.13,"close":7.15,"pre_close":7.18,"change":-0.03,"pct_chg":-0.4178,"vol":138362.2,"amount":99454.484},{"ts_code":"601226.SH","trade_date":"20251010","open":7.13,"high":7.3,"low":7.1,"close":7.3,"pre_close":7.15,"change":0.15,"pct_chg":2.0979,"vol":196969.6,"amount":142504.582},{"ts_code":"601226.SH","trade_date":"20251013","open":7.08,"high":7.33,"low":7.03,"close":7.29,"pre_close":7.3,"change":-0.01,"pct_chg":-0.137,"vol":196993.5,"amount":142030.237},{"ts_code":"601226.SH","trade_date":"20251014","open":7.46,"high":7.68,"low":7.35,"close":7.41,"pre_close":7.29,"change":0.12,"pct_chg":1.6461,"vol":389776.5,"amount":292457.277},{"ts_code":"601226.SH","trade_date":"20251015","open":7.53,"high":7.77,"low":7.39,"close":7.77,"pre_close":7.41,"change":0.36,"pct_chg":4.8583,"vol":435188.5,"amount":330739.582},{"ts_code":"601226.SH","trade_date":"20251016","open":7.8,"high":7.8,"low":7.4,"close":7.44,"pre_close":7.77,"change":-0.33,"pct_chg":-4.2471,"vol":281494.66,"amount":212179.408},{"ts_code":"601226.SH","trade_date":"20251017","open":7.45,"high":7.53,"low":7.18,"close":7.19,"pre_close":7.44,"change":-0.25,"pct_chg":-3.3602,"vol":206461.74,"amount":150483.796},{"ts_code":"601226.SH","trade_date":"20251020","open":7.27,"high":7.37,"low":7.22,"close":7.33,"pre_close":7.19,"change":0.14,"pct_chg":1.9471,"vol":130693.78,"amount":95290.374},{"ts_code":"601226.SH","trade_date":"20251021","open":7.28,"high":7.66,"low":7.28,"close":7.61,"pre_close":7.33,"change":0.28,"pct_chg":3.8199,"vol":239088.46,"amount":180058.399},{"ts_code":"601226.SH","trade_date":"20251022","open":7.6,"high":7.62,"low":7.49,"close":7.52,"pre_close":7.61,"change":-0.09,"pct_chg":-1.1827,"vol":128878.72,"amount":97264.113},{"ts_code":"601226.SH","trade_date":"20251023","open":7.44,"high":7.59,"low":7.41,"close":7.56,"pre_close":7.52,"change":0.04,"pct_chg":0.5319,"vol":137771.0,"amount":103323.519},{"ts_code":"601226.SH","trade_date":"20251024","open":7.55,"high":7.58,"low":7.44,"close":7.5,"pre_close":7.56,"change":-0.06,"pct_chg":-0.7937,"vol":125577.0,"amount":94239.892},{"ts_code":"601226.SH","trade_date":"20251027","open":7.5,"high":7.72,"low":7.49,"close":7.67,"pre_close":7.5,"change":0.17,"pct_chg":2.2667,"vol":181906.82,"amount":138436.883},{"ts_code":"601226.SH","trade_date":"20251028","open":7.71,"high":7.72,"low":7.59,"close":7.6,"pre_close":7.67,"change":-0.07,"pct_chg":-0.9126,"vol":147414.0,"amount":112760.671},{"ts_code":"601226.SH","trade_date":"20251029","open":7.49,"high":7.76,"low":7.48,"close":7.58,"pre_close":7.6,"change":-0.02,"pct_chg":-0.2632,"vol":179441.5,"amount":136584.835},{"ts_code":"601226.SH","trade_date":"20251030","open":7.56,"high":7.74,"low":7.52,"close":7.66,"pre_close":7.58,"change":0.08,"pct_chg":1.0554,"vol":230200.34,"amount":176020.916},{"ts_code":"601226.SH","trade_date":"20251031","open":7.56,"high":7.63,"low":7.42,"close":7.42,"pre_close":7.66,"change":-0.24,"pct_chg":-3.1332,"vol":220601.0,"amount":165575.247},{"ts_code":"601226.SH","trade_date":"20251103","open":7.42,"high":7.55,"low":7.32,"close":7.47,"pre_close":7.42,"change":0.05,"pct_chg":0.6739,"vol":178979.03,"amount":132676.736},{"ts_code":"601226.SH","trade_date":"20251104","open":7.47,"high":7.62,"low":7.44,"close":7.57,"pre_close":7.47,"change":0.1,"pct_chg":1.3387,"vol":176021.5,"amount":132870.664},{"ts_code":"601226.SH","trade_date":"20251105","open":7.53,"high":7.83,"low":7.45,"close":7.76,"pre_close":7.57,"change":0.19,"pct_chg":2.5099,"vol":359756.99,"amount":277153.973},{"ts_code":"601226.SH","trade_date":"20251106","open":7.82,"high":7.97,"low":7.75,"close":7.79,"pre_close":7.76,"change":0.03,"pct_chg":0.3866,"vol":318272.97,"amount":249727.587},{"ts_code":"601226.SH","trade_date":"20251107","open":7.71,"high":7.95,"low":7.68,"close":7.72,"pre_close":7.79,"change":-0.07,"pct_chg":-0.8986,"vol":199109.0,"amount":155082.376},{"ts_code":"601226.SH","trade_date":"20251110","open":8.49,"high":8.49,"low":8.34,"close":8.49,"pre_close":7.72,"change":0.77,"pct_chg":9.9741,"vol":393160.75,"amount":333166.217},{"ts_code":"601226.SH","trade_date":"20251111","open":8.51,"high":8.66,"low":8.22,"close":8.33,"pre_close":8.49,"change":-0.16,"pct_chg":-1.8846,"vol":990446.25,"amount":826578.704},{"ts_code":"601226.SH","trade_date":"20251112","open":8.23,"high":8.31,"low":7.88,"close":7.99,"pre_close":8.33,"change":-0.34,"pct_chg":-4.0816,"vol":568096.81,"amount":455351.164},{"ts_code":"601226.SH","trade_date":"20251113","open":7.92,"high":8.37,"low":7.82,"close":8.21,"pre_close":7.99,"change":0.22,"pct_chg":2.7534,"vol":670817.0,"amount":548289.439},{"ts_code":"601226.SH","trade_date":"20251114","open":8.21,"high":8.22,"low":7.98,"close":8.02,"pre_close":8.21,"change":-0.19,"pct_chg":-2.3143,"vol":370102.0,"amount":298199.733},{"ts_code":"601226.SH","trade_date":"20251117","open":7.93,"high":7.98,"low":7.61,"close":7.76,"pre_close":8.02,"change":-0.26,"pct_chg":-3.2419,"vol":369686.64,"amount":286725.522},{"ts_code":"601226.SH","trade_date":"20251118","open":7.75,"high":7.76,"low":7.37,"close":7.42,"pre_close":7.76,"change":-0.34,"pct_chg":-4.3814,"vol":288385.0,"amount":215801.808},{"ts_code":"601226.SH","trade_date":"20251119","open":7.42,"high":7.77,"low":7.3,"close":7.59,"pre_close":7.42,"change":0.17,"pct_chg":2.2911,"vol":354815.81,"amount":269610.654},{"ts_code":"601226.SH","trade_date":"20251120","open":7.66,"high":7.85,"low":7.48,"close":7.57,"pre_close":7.59,"change":-0.02,"pct_chg":-0.2635,"vol":221715.48,"amount":169391.99},{"ts_code":"601226.SH","trade_date":"20251121","open":7.46,"high":7.54,"low":7.14,"close":7.15,"pre_close":7.57,"change":-0.42,"pct_chg":-5.5482,"vol":255702.0,"amount":186364.455},{"ts_code":"601226.SH","trade_date":"20251124","open":7.16,"high":7.32,"low":7.04,"close":7.17,"pre_close":7.15,"change":0.02,"pct_chg":0.2797,"vol":193569.5,"amount":138976.095},{"ts_code":"601226.SH","trade_date":"20251125","open":7.23,"high":7.4,"low":7.17,"close":7.29,"pre_close":7.17,"change":0.12,"pct_chg":1.6736,"vol":178249.0,"amount":129561.437},{"ts_code":"601226.SH","trade_date":"20251126","open":7.27,"high":7.34,"low":7.21,"close":7.28,"pre_close":7.29,"change":-0.01,"pct_chg":-0.1372,"vol":129799.0,"amount":94417.531},{"ts_code":"601226.SH","trade_date":"20251127","open":7.22,"high":7.31,"low":7.2,"close":7.22,"pre_close":7.28,"change":-0.06,"pct_chg":-0.8242,"vol":84995.0,"amount":61648.457},{"ts_code":"601226.SH","trade_date":"20251128","open":7.22,"high":7.59,"low":7.19,"close":7.54,"pre_close":7.22,"change":0.32,"pct_chg":4.4321,"vol":288226.02,"amount":216078.22},{"ts_code":"601226.SH","trade_date":"20251201","open":7.54,"high":7.95,"low":7.5,"close":7.77,"pre_close":7.54,"change":0.23,"pct_chg":3.0504,"vol":308722.08,"amount":239759.048},{"ts_code":"601226.SH","trade_date":"20251202","open":7.74,"high":7.76,"low":7.59,"close":7.69,"pre_close":7.77,"change":-0.08,"pct_chg":-1.0296,"vol":130361.72,"amount":99914.974},{"ts_code":"601226.SH","trade_date":"20251203","open":7.69,"high":7.85,"low":7.64,"close":7.75,"pre_close":7.69,"change":0.06,"pct_chg":0.7802,"vol":164372.1,"amount":127282.606},{"ts_code":"601226.SH","trade_date":"20251204","open":7.71,"high":7.76,"low":7.6,"close":7.61,"pre_close":7.75,"change":-0.14,"pct_chg":-1.8065,"vol":100013.28,"amount":76553.107},{"ts_code":"601226.SH","trade_date":"20251205","open":7.61,"high":7.83,"low":7.59,"close":7.78,"pre_close":7.61,"change":0.17,"pct_chg":2.2339,"vol":118431.21,"amount":91778.491},{"ts_code":"601226.SH","trade_date":"20251208","open":7.76,"high":7.88,"low":7.74,"close":7.78,"pre_close":7.78,"change":0.0,"pct_chg":0.0,"vol":154154.0,"amount":120316.961},{"ts_code":"601226.SH","trade_date":"20251209","open":7.72,"high":7.83,"low":7.67,"close":7.8,"pre_close":7.78,"change":0.02,"pct_chg":0.2571,"vol":136959.64,"amount":106115.604},{"ts_code":"601226.SH","trade_date":"20251210","open":7.79,"high":7.79,"low":7.65,"close":7.78,"pre_close":7.8,"change":-0.02,"pct_chg":-0.2564,"vol":109967.28,"amount":84872.064},{"ts_code":"601226.SH","trade_date":"20251211","open":7.9,"high":8.05,"low":7.81,"close":7.88,"pre_close":7.78,"change":0.1,"pct_chg":1.2853,"vol":224970.76,"amount":178854.106},{"ts_code":"601226.SH","trade_date":"20251212","open":7.87,"high":8.04,"low":7.85,"close":8.0,"pre_close":7.88,"change":0.12,"pct_chg":1.5228,"vol":180232.5,"amount":143913.657},{"ts_code":"601226.SH","trade_date":"20251215","open":8.16,"high":8.33,"low":8.1,"close":8.23,"pre_close":8.0,"change":0.23,"pct_chg":2.875,"vol":305570.82,"amount":250825.14},{"ts_code":"601226.SH","trade_date":"20251216","open":8.22,"high":8.22,"low":7.87,"close":7.9,"pre_close":8.23,"change":-0.33,"pct_chg":-4.0097,"vol":223535.61,"amount":178130.032},{"ts_code":"601226.SH","trade_date":"20251217","open":7.86,"high":7.94,"low":7.69,"close":7.91,"pre_close":7.9,"change":0.01,"pct_chg":0.1266,"vol":152927.0,"amount":119485.544},{"ts_code":"601226.SH","trade_date":"20251218","open":7.82,"high":7.89,"low":7.76,"close":7.87,"pre_close":7.91,"change":-0.04,"pct_chg":-0.5057,"vol":156503.0,"amount":122387.66},{"ts_code":"601226.SH","trade_date":"20251219","open":7.86,"high":8.05,"low":7.83,"close":7.88,"pre_close":7.87,"change":0.01,"pct_chg":0.1271,"vol":183392.0,"amount":145396.262},{"ts_code":"601226.SH","trade_date":"20251222","open":7.92,"high":8.1,"low":7.89,"close":8.01,"pre_close":7.88,"change":0.13,"pct_chg":1.6497,"vol":164523.52,"amount":131271.795},{"ts_code":"601226.SH","trade_date":"20251223","open":7.98,"high":8.04,"low":7.81,"close":7.86,"pre_close":8.01,"change":-0.15,"pct_chg":-1.8727,"vol":111367.0,"amount":88007.077},{"ts_code":"601226.SH","trade_date":"20251224","open":7.88,"high":8.0,"low":7.78,"close":7.93,"pre_close":7.86,"change":0.07,"pct_chg":0.8906,"vol":105946.0,"amount":83820.407},{"ts_code":"601226.SH","trade_date":"20251225","open":7.92,"high":8.1,"low":7.86,"close":8.01,"pre_close":7.93,"change":0.08,"pct_chg":1.0088,"vol":147984.82,"amount":118640.045},{"ts_code":"601226.SH","trade_date":"20251226","open":8.2,"high":8.25,"low":7.95,"close":8.05,"pre_close":8.01,"change":0.04,"pct_chg":0.4994,"vol":241835.0,"amount":195874.695},{"ts_code":"601226.SH","trade_date":"20251229","open":8.05,"high":8.25,"low":7.98,"close":8.16,"pre_close":8.05,"change":0.11,"pct_chg":1.3665,"vol":244251.47,"amount":198271.378},{"ts_code":"601226.SH","trade_date":"20251230","open":8.08,"high":8.13,"low":7.95,"close":7.95,"pre_close":8.16,"change":-0.21,"pct_chg":-2.5735,"vol":170275.1,"amount":136478.848},{"ts_code":"601226.SH","trade_date":"20251231","open":7.94,"high":7.98,"low":7.73,"close":7.84,"pre_close":7.95,"change":-0.11,"pct_chg":-1.3836,"vol":166290.5,"amount":130229.731},{"ts_code":"601226.SH","trade_date":"20260105","open":7.84,"high":8.02,"low":7.77,"close":7.86,"pre_close":7.84,"change":0.02,"pct_chg":0.2551,"vol":164497.5,"amount":130381.312},{"ts_code":"601226.SH","trade_date":"20260106","open":7.88,"high":8.18,"low":7.83,"close":8.15,"pre_close":7.86,"change":0.29,"pct_chg":3.6896,"vol":249156.35,"amount":200427.965},{"ts_code":"601226.SH","trade_date":"20260107","open":8.09,"high":8.27,"low":8.04,"close":8.2,"pre_close":8.15,"change":0.05,"pct_chg":0.6135,"vol":221837.83,"amount":181909.509},{"ts_code":"601226.SH","trade_date":"20260108","open":8.18,"high":8.55,"low":8.15,"close":8.36,"pre_close":8.2,"change":0.16,"pct_chg":1.9512,"vol":260179.0,"amount":217942.174},{"ts_code":"601226.SH","trade_date":"20260109","open":8.3,"high":9.2,"low":8.3,"close":8.93,"pre_close":8.36,"change":0.57,"pct_chg":6.8182,"vol":849305.14,"amount":761819.797},{"ts_code":"601226.SH","trade_date":"20260112","open":8.95,"high":9.1,"low":8.79,"close":8.84,"pre_close":8.93,"change":-0.09,"pct_chg":-1.0078,"vol":541215.0,"amount":482475.039},{"ts_code":"601226.SH","trade_date":"20260113","open":8.86,"high":9.28,"low":8.69,"close":9.02,"pre_close":8.84,"change":0.18,"pct_chg":2.0362,"vol":499313.64,"amount":447986.648},{"ts_code":"601226.SH","trade_date":"20260114","open":9.0,"high":9.17,"low":8.8,"close":8.92,"pre_close":9.02,"change":-0.1,"pct_chg":-1.1086,"vol":385142.89,"amount":346003.711},{"ts_code":"601226.SH","trade_date":"20260115","open":8.9,"high":9.04,"low":8.63,"close":8.74,"pre_close":8.92,"change":-0.18,"pct_chg":-2.0179,"vol":247434.17,"amount":216312.451},{"ts_code":"601226.SH","trade_date":"20260116","open":8.81,"high":8.98,"low":8.71,"close":8.73,"pre_close":8.74,"change":-0.01,"pct_chg":-0.1144,"vol":199654.87,"amount":175902.531},{"ts_code":"601226.SH","trade_date":"20260119","open":8.7,"high":9.18,"low":8.69,"close":9.07,"pre_close":8.73,"change":0.34,"pct_chg":3.8946,"vol":399047.81,"amount":361792.603},{"ts_code":"601226.SH","trade_date":"20260120","open":9.09,"high":9.16,"low":8.86,"close":8.96,"pre_close":9.07,"change":-0.11,"pct_chg":-1.2128,"vol":202632.66,"amount":181629.091},{"ts_code":"601226.SH","trade_date":"20260121","open":9.01,"high":9.63,"low":8.86,"close":9.4,"pre_close":8.96,"change":0.44,"pct_chg":4.9107,"vol":499390.95,"amount":464207.895},{"ts_code":"601226.SH","trade_date":"20260122","open":9.4,"high":9.65,"low":9.27,"close":9.33,"pre_close":9.4,"change":-0.07,"pct_chg":-0.7447,"vol":361108.51,"amount":339010.397},{"ts_code":"601226.SH","trade_date":"20260123","open":9.6,"high":10.2,"low":9.51,"close":9.65,"pre_close":9.33,"change":0.32,"pct_chg":3.4298,"vol":486314.48,"amount":474321.818},{"ts_code":"601226.SH","trade_date":"20260126","open":9.53,"high":10.62,"low":9.47,"close":10.62,"pre_close":9.65,"change":0.97,"pct_chg":10.0518,"vol":736918.56,"amount":762212.933},{"ts_code":"601226.SH","trade_date":"20260127","open":10.39,"high":11.68,"low":10.01,"close":11.4,"pre_close":10.62,"change":0.78,"pct_chg":7.3446,"vol":1433435.98,"amount":1547995.582},{"ts_code":"601226.SH","trade_date":"20260128","open":11.34,"high":11.37,"low":10.69,"close":10.92,"pre_close":11.4,"change":-0.48,"pct_chg":-4.2105,"vol":859943.53,"amount":939511.605},{"ts_code":"601226.SH","trade_date":"20260129","open":10.8,"high":11.08,"low":10.39,"close":10.49,"pre_close":10.92,"change":-0.43,"pct_chg":-3.9377,"vol":595588.48,"amount":634287.854},{"ts_code":"601226.SH","trade_date":"20260130","open":10.2,"high":11.54,"low":10.13,"close":11.21,"pre_close":10.49,"change":0.72,"pct_chg":6.8637,"vol":952861.92,"amount":1040309.692},{"ts_code":"601226.SH","trade_date":"20260202","open":10.97,"high":11.11,"low":10.62,"close":10.7,"pre_close":11.21,"change":-0.51,"pct_chg":-4.5495,"vol":689022.17,"amount":748413.27},{"ts_code":"601226.SH","trade_date":"20260203","open":10.88,"high":11.77,"low":10.7,"close":11.57,"pre_close":10.7,"change":0.87,"pct_chg":8.1308,"vol":868653.92,"amount":995741.476},{"ts_code":"601226.SH","trade_date":"20260204","open":11.58,"high":12.73,"low":11.58,"close":12.73,"pre_close":11.57,"change":1.16,"pct_chg":10.0259,"vol":1441789.72,"amount":1795052.965},{"ts_code":"601226.SH","trade_date":"20260205","open":12.26,"high":12.54,"low":11.46,"close":11.46,"pre_close":12.73,"change":-1.27,"pct_chg":-9.9764,"vol":1233419.18,"amount":1454690.646},{"ts_code":"601226.SH","trade_date":"20260206","open":11.11,"high":11.36,"low":10.89,"close":10.98,"pre_close":11.46,"change":-0.48,"pct_chg":-4.1885,"vol":814717.98,"amount":901515.131},{"ts_code":"601226.SH","trade_date":"20260209","open":10.93,"high":11.39,"low":10.93,"close":11.04,"pre_close":10.98,"change":0.06,"pct_chg":0.5464,"vol":622823.91,"amount":695013.714},{"ts_code":"601226.SH","trade_date":"20260210","open":10.87,"high":11.1,"low":10.45,"close":10.72,"pre_close":11.04,"change":-0.32,"pct_chg":-2.8986,"vol":641721.05,"amount":689035.062},{"ts_code":"601226.SH","trade_date":"20260211","open":10.56,"high":10.82,"low":10.35,"close":10.37,"pre_close":10.72,"change":-0.35,"pct_chg":-3.2649,"vol":490919.3,"amount":515986.775},{"ts_code":"601226.SH","trade_date":"20260212","open":10.3,"high":10.97,"low":10.18,"close":10.85,"pre_close":10.37,"change":0.48,"pct_chg":4.6287,"vol":598545.42,"amount":636340.474},{"ts_code":"601226.SH","trade_date":"20260213","open":11.07,"high":11.19,"low":10.69,"close":10.69,"pre_close":10.85,"change":-0.16,"pct_chg":-1.4747,"vol":358137.0,"amount":389963.873},{"ts_code":"601226.SH","trade_date":"20260224","open":10.83,"high":11.73,"low":10.75,"close":11.5,"pre_close":10.69,"change":0.81,"pct_chg":7.5772,"vol":652572.88,"amount":745921.323},{"ts_code":"601226.SH","trade_date":"20260225","open":11.52,"high":11.96,"low":11.3,"close":11.49,"pre_close":11.5,"change":-0.01,"pct_chg":-0.087,"vol":504961.04,"amount":584907.549},{"ts_code":"601226.SH","trade_date":"20260226","open":11.63,"high":11.68,"low":11.3,"close":11.59,"pre_close":11.49,"change":0.1,"pct_chg":0.8703,"vol":383095.5,"amount":441443.73},{"ts_code":"601226.SH","trade_date":"20260227","open":11.67,"high":12.54,"low":11.59,"close":12.45,"pre_close":11.59,"change":0.86,"pct_chg":7.4202,"vol":736368.89,"amount":890206.47},{"ts_code":"601226.SH","trade_date":"20260302","open":12.25,"high":12.5,"low":11.79,"close":11.92,"pre_close":12.45,"change":-0.53,"pct_chg":-4.257,"vol":568570.91,"amount":687551.881},{"ts_code":"601226.SH","trade_date":"20260303","open":11.83,"high":11.95,"low":10.79,"close":10.82,"pre_close":11.92,"change":-1.1,"pct_chg":-9.2282,"vol":582779.05,"amount":651220.796},{"ts_code":"601226.SH","trade_date":"20260304","open":10.79,"high":11.53,"low":10.79,"close":11.06,"pre_close":10.82,"change":0.24,"pct_chg":2.2181,"vol":556083.97,"amount":620891.546},{"ts_code":"601226.SH","trade_date":"20260305","open":11.28,"high":12.17,"low":11.13,"close":11.82,"pre_close":11.06,"change":0.76,"pct_chg":6.8716,"vol":906580.36,"amount":1068278.17},{"ts_code":"601226.SH","trade_date":"20260306","open":12.07,"high":12.07,"low":11.33,"close":11.44,"pre_close":11.82,"change":-0.38,"pct_chg":-3.2149,"vol":726435.69,"amount":844267.222},{"ts_code":"601226.SH","trade_date":"20260309","open":11.2,"high":11.35,"low":10.83,"close":11.2,"pre_close":11.44,"change":-0.24,"pct_chg":-2.0979,"vol":557229.84,"amount":619502.027},{"ts_code":"601226.SH","trade_date":"20260310","open":11.25,"high":12.32,"low":11.25,"close":12.0,"pre_close":11.2,"change":0.8,"pct_chg":7.1429,"vol":973193.72,"amount":1165112.924},{"ts_code":"601226.SH","trade_date":"20260311","open":12.1,"high":12.34,"low":11.84,"close":11.85,"pre_close":12.0,"change":-0.15,"pct_chg":-1.25,"vol":943460.99,"amount":1137064.317},{"ts_code":"601226.SH","trade_date":"20260312","open":11.9,"high":11.95,"low":11.35,"close":11.62,"pre_close":11.85,"change":-0.23,"pct_chg":-1.9409,"vol":615809.24,"amount":714857.033},{"ts_code":"601226.SH","trade_date":"20260313","open":11.66,"high":11.85,"low":10.9,"close":10.94,"pre_close":11.62,"change":-0.68,"pct_chg":-5.852,"vol":577289.01,"amount":650954.256},{"ts_code":"601226.SH","trade_date":"20260316","open":10.83,"high":10.88,"low":10.11,"close":10.6,"pre_close":10.94,"change":-0.34,"pct_chg":-3.1079,"vol":619119.18,"amount":645916.973},{"ts_code":"601226.SH","trade_date":"20260317","open":10.81,"high":10.83,"low":9.87,"close":9.92,"pre_close":10.6,"change":-0.68,"pct_chg":-6.4151,"vol":636041.62,"amount":646843.077},{"ts_code":"601226.SH","trade_date":"20260318","open":9.87,"high":9.98,"low":9.49,"close":9.73,"pre_close":9.92,"change":-0.19,"pct_chg":-1.9153,"vol":437132.4,"amount":423348.535},{"ts_code":"601226.SH","trade_date":"20260319","open":9.58,"high":9.7,"low":9.36,"close":9.4,"pre_close":9.73,"change":-0.33,"pct_chg":-3.3916,"vol":309487.77,"amount":293557.59},{"ts_code":"601226.SH","trade_date":"20260320","open":9.49,"high":9.57,"low":9.18,"close":9.18,"pre_close":9.4,"change":-0.22,"pct_chg":-2.3404,"vol":262993.17,"amount":246241.214},{"ts_code":"601226.SH","trade_date":"20260323","open":9.1,"high":9.3,"low":8.8,"close":8.87,"pre_close":9.18,"change":-0.31,"pct_chg":-3.3769,"vol":353704.85,"amount":319865.47},{"ts_code":"601226.SH","trade_date":"20260324","open":9.4,"high":9.76,"low":9.4,"close":9.76,"pre_close":8.87,"change":0.89,"pct_chg":10.0338,"vol":470438.75,"amount":455895.064},{"ts_code":"601226.SH","trade_date":"20260325","open":10.1,"high":10.24,"low":9.75,"close":9.81,"pre_close":9.76,"change":0.05,"pct_chg":0.5123,"vol":870631.15,"amount":865138.401},{"ts_code":"601226.SH","trade_date":"20260326","open":10.05,"high":10.15,"low":9.37,"close":9.42,"pre_close":9.81,"change":-0.39,"pct_chg":-3.9755,"vol":550199.95,"amount":531237.742},{"ts_code":"601226.SH","trade_date":"20260327","open":9.25,"high":9.55,"low":9.18,"close":9.39,"pre_close":9.42,"change":-0.03,"pct_chg":-0.3185,"vol":352803.25,"amount":331687.689},{"ts_code":"601226.SH","trade_date":"20260330","open":9.34,"high":9.39,"low":9.13,"close":9.3,"pre_close":9.39,"change":-0.09,"pct_chg":-0.9585,"vol":278801.0,"amount":258085.949},{"ts_code":"601226.SH","trade_date":"20260331","open":9.31,"high":9.47,"low":9.06,"close":9.07,"pre_close":9.3,"change":-0.23,"pct_chg":-2.4731,"vol":279050.52,"amount":257205.645},{"ts_code":"601226.SH","trade_date":"20260401","open":9.25,"high":9.33,"low":9.16,"close":9.25,"pre_close":9.07,"change":0.18,"pct_chg":1.9846,"vol":260256.24,"amount":240712.766},{"ts_code":"601226.SH","trade_date":"20260402","open":9.21,"high":9.35,"low":8.92,"close":8.98,"pre_close":9.25,"change":-0.27,"pct_chg":-2.9189,"vol":234858.87,"amount":213719.132},{"ts_code":"601226.SH","trade_date":"20260403","open":8.98,"high":9.06,"low":8.65,"close":8.67,"pre_close":8.98,"change":-0.31,"pct_chg":-3.4521,"vol":237446.68,"amount":207752.783},{"ts_code":"601226.SH","trade_date":"20260407","open":8.7,"high":8.83,"low":8.66,"close":8.75,"pre_close":8.67,"change":0.08,"pct_chg":0.9227,"vol":169457.01,"amount":148384.694},{"ts_code":"601226.SH","trade_date":"20260408","open":9.11,"high":9.34,"low":9.11,"close":9.32,"pre_close":8.75,"change":0.57,"pct_chg":6.5143,"vol":273287.92,"amount":252885.102},{"ts_code":"601226.SH","trade_date":"20260409","open":9.25,"high":9.27,"low":9.09,"close":9.13,"pre_close":9.32,"change":-0.19,"pct_chg":-2.0386,"vol":189779.29,"amount":173666.071},{"ts_code":"601226.SH","trade_date":"20260410","open":9.21,"high":9.28,"low":9.13,"close":9.17,"pre_close":9.13,"change":0.04,"pct_chg":0.4381,"vol":157517.09,"amount":145060.706},{"ts_code":"601226.SH","trade_date":"20260413","open":9.17,"high":9.41,"low":9.14,"close":9.32,"pre_close":9.17,"change":0.15,"pct_chg":1.6358,"vol":212578.49,"amount":197513.024},{"ts_code":"601226.SH","trade_date":"20260414","open":9.33,"high":9.36,"low":9.17,"close":9.27,"pre_close":9.32,"change":-0.05,"pct_chg":-0.5365,"vol":170728.68,"amount":157964.937},{"ts_code":"601226.SH","trade_date":"20260415","open":9.31,"high":9.52,"low":9.22,"close":9.29,"pre_close":9.27,"change":0.02,"pct_chg":0.2157,"vol":320570.27,"amount":300133.665},{"ts_code":"601226.SH","trade_date":"20260416","open":9.27,"high":9.43,"low":9.12,"close":9.42,"pre_close":9.29,"change":0.13,"pct_chg":1.3994,"vol":230497.0,"amount":215405.335},{"ts_code":"601226.SH","trade_date":"20260417","open":9.42,"high":9.64,"low":9.42,"close":9.59,"pre_close":9.42,"change":0.17,"pct_chg":1.8047,"vol":289720.8,"amount":276637.016},{"ts_code":"601226.SH","trade_date":"20260420","open":9.65,"high":9.65,"low":9.48,"close":9.57,"pre_close":9.59,"change":-0.02,"pct_chg":-0.2086,"vol":233914.4,"amount":223705.773},{"ts_code":"601226.SH","trade_date":"20260421","open":9.56,"high":9.56,"low":9.4,"close":9.51,"pre_close":9.57,"change":-0.06,"pct_chg":-0.627,"vol":161348.15,"amount":153212.364},{"ts_code":"601226.SH","trade_date":"20260422","open":9.52,"high":9.59,"low":9.44,"close":9.52,"pre_close":9.51,"change":0.01,"pct_chg":0.1052,"vol":182622.0,"amount":173685.882},{"ts_code":"601226.SH","trade_date":"20260423","open":9.55,"high":9.61,"low":9.3,"close":9.4,"pre_close":9.52,"change":-0.12,"pct_chg":-1.2605,"vol":176416.19,"amount":166378.587},{"ts_code":"601226.SH","trade_date":"20260424","open":9.4,"high":9.4,"low":9.17,"close":9.26,"pre_close":9.4,"change":-0.14,"pct_chg":-1.4894,"vol":150567.51,"amount":139587.939},{"ts_code":"601226.SH","trade_date":"20260427","open":9.23,"high":9.51,"low":9.15,"close":9.33,"pre_close":9.26,"change":0.07,"pct_chg":0.7559,"vol":186633.0,"amount":173879.815},{"ts_code":"601226.SH","trade_date":"20260428","open":9.38,"high":9.38,"low":8.98,"close":8.98,"pre_close":9.33,"change":-0.35,"pct_chg":-3.7513,"vol":221461.0,"amount":201319.757},{"ts_code":"601226.SH","trade_date":"20260429","open":8.89,"high":9.17,"low":8.83,"close":9.09,"pre_close":8.98,"change":0.11,"pct_chg":1.2249,"vol":160430.0,"amount":145274.713},{"ts_code":"601226.SH","trade_date":"20260430","open":9.05,"high":9.14,"low":8.76,"close":8.86,"pre_close":9.09,"change":-0.23,"pct_chg":-2.5303,"vol":190917.27,"amount":169551.073},{"ts_code":"601226.SH","trade_date":"20260506","open":8.9,"high":9.07,"low":8.89,"close":8.97,"pre_close":8.86,"change":0.11,"pct_chg":1.2415,"vol":196317.5,"amount":176496.668},{"ts_code":"601226.SH","trade_date":"20260507","open":8.95,"high":9.21,"low":8.95,"close":9.12,"pre_close":8.97,"change":0.15,"pct_chg":1.6722,"vol":180608.54,"amount":163949.802},{"ts_code":"601226.SH","trade_date":"20260508","open":9.11,"high":9.22,"low":9.02,"close":9.16,"pre_close":9.12,"change":0.04,"pct_chg":0.4386,"vol":157253.36,"amount":143474.167},{"ts_code":"601226.SH","trade_date":"20260511","open":9.25,"high":9.33,"low":9.15,"close":9.17,"pre_close":9.16,"change":0.01,"pct_chg":0.1092,"vol":197217.45,"amount":182047.901},{"ts_code":"601226.SH","trade_date":"20260512","open":9.23,"high":9.3,"low":8.98,"close":9.02,"pre_close":9.17,"change":-0.15,"pct_chg":-1.6358,"vol":220065.0,"amount":200436.029},{"ts_code":"601226.SH","trade_date":"20260513","open":9.0,"high":9.45,"low":8.96,"close":9.3,"pre_close":9.02,"change":0.28,"pct_chg":3.1042,"vol":360507.68,"amount":336992.791},{"ts_code":"601226.SH","trade_date":"20260514","open":9.32,"high":9.38,"low":8.86,"close":8.86,"pre_close":9.3,"change":-0.44,"pct_chg":-4.7312,"vol":260734.4,"amount":236396.002},{"ts_code":"601226.SH","trade_date":"20260515","open":8.87,"high":8.94,"low":8.56,"close":8.63,"pre_close":8.86,"change":-0.23,"pct_chg":-2.5959,"vol":234833.85,"amount":204585.16},{"ts_code":"601226.SH","trade_date":"20260518","open":8.61,"high":8.68,"low":8.45,"close":8.59,"pre_close":8.63,"change":-0.04,"pct_chg":-0.4635,"vol":152102.0,"amount":130392.253},{"ts_code":"601226.SH","trade_date":"20260519","open":8.58,"high":8.75,"low":8.46,"close":8.74,"pre_close":8.59,"change":0.15,"pct_chg":1.7462,"vol":150903.5,"amount":129792.806},{"ts_code":"601226.SH","trade_date":"20260520","open":8.7,"high":8.7,"low":8.4,"close":8.48,"pre_close":8.74,"change":-0.26,"pct_chg":-2.9748,"vol":181255.9,"amount":153287.991},{"ts_code":"601226.SH","trade_date":"20260521","open":8.43,"high":8.52,"low":8.08,"close":8.12,"pre_close":8.48,"change":-0.36,"pct_chg":-4.2453,"vol":191008.14,"amount":158310.352},{"ts_code":"601226.SH","trade_date":"20260522","open":8.19,"high":8.28,"low":8.07,"close":8.25,"pre_close":8.12,"change":0.13,"pct_chg":1.601,"vol":135781.38,"amount":111584.386},{"ts_code":"601226.SH","trade_date":"20260525","open":8.19,"high":8.38,"low":8.19,"close":8.28,"pre_close":8.25,"change":0.03,"pct_chg":0.3636,"vol":102359.0,"amount":84868.326},{"ts_code":"601226.SH","trade_date":"20260526","open":8.2,"high":8.22,"low":8.0,"close":8.12,"pre_close":8.28,"change":-0.16,"pct_chg":-1.9324,"vol":125754.81,"amount":101512.548},{"ts_code":"601226.SH","trade_date":"20260527","open":8.1,"high":8.19,"low":7.98,"close":8.03,"pre_close":8.12,"change":-0.09,"pct_chg":-1.1084,"vol":112576.43,"amount":90932.286},{"ts_code":"601226.SH","trade_date":"20260528","open":7.98,"high":8.14,"low":7.92,"close":8.08,"pre_close":8.03,"change":0.05,"pct_chg":0.6227,"vol":117779.0,"amount":94603.371},{"ts_code":"601226.SH","trade_date":"20260529","open":8.08,"high":8.16,"low":7.85,"close":7.86,"pre_close":8.08,"change":-0.22,"pct_chg":-2.7228,"vol":125516.0,"amount":100204.857},{"ts_code":"601226.SH","trade_date":"20260601","open":7.81,"high":8.0,"low":7.72,"close":7.9,"pre_close":7.86,"change":0.04,"pct_chg":0.5089,"vol":118014.0,"amount":93249.334},{"ts_code":"601226.SH","trade_date":"20260602","open":7.86,"high":7.94,"low":7.63,"close":7.66,"pre_close":7.9,"change":-0.24,"pct_chg":-3.038,"vol":121535.04,"amount":93570.341},{"ts_code":"601226.SH","trade_date":"20260603","open":7.65,"high":7.72,"low":7.51,"close":7.58,"pre_close":7.66,"change":-0.08,"pct_chg":-1.0444,"vol":121845.5,"amount":92892.799},{"ts_code":"601226.SH","trade_date":"20260604","open":7.62,"high":7.64,"low":7.4,"close":7.46,"pre_close":7.58,"change":-0.12,"pct_chg":-1.5831,"vol":117345.0,"amount":87714.074},{"ts_code":"601226.SH","trade_date":"20260605","open":7.45,"high":7.51,"low":7.3,"close":7.43,"pre_close":7.46,"change":-0.03,"pct_chg":-0.4021,"vol":112272.16,"amount":83191.743},{"ts_code":"601226.SH","trade_date":"20260608","open":7.22,"high":7.37,"low":7.0,"close":7.11,"pre_close":7.43,"change":-0.32,"pct_chg":-4.3069,"vol":147464.63,"amount":105793.255},{"ts_code":"601226.SH","trade_date":"20260609","open":7.18,"high":7.23,"low":7.06,"close":7.15,"pre_close":7.11,"change":0.04,"pct_chg":0.5626,"vol":91827.79,"amount":65403.195},{"ts_code":"601226.SH","trade_date":"20260610","open":7.1,"high":7.12,"low":6.83,"close":6.91,"pre_close":7.15,"change":-0.24,"pct_chg":-3.3566,"vol":127106.13,"amount":88165.127},{"ts_code":"601226.SH","trade_date":"20260611","open":6.93,"high":6.93,"low":6.77,"close":6.85,"pre_close":6.91,"change":-0.06,"pct_chg":-0.8683,"vol":102372.5,"amount":69953.762},{"ts_code":"601226.SH","trade_date":"20260612","open":6.89,"high":7.05,"low":6.88,"close":6.98,"pre_close":6.85,"change":0.13,"pct_chg":1.8978,"vol":120137.0,"amount":83809.324},{"ts_code":"601226.SH","trade_date":"20260615","open":7.06,"high":7.2,"low":7.03,"close":7.11,"pre_close":6.98,"change":0.13,"pct_chg":1.8625,"vol":100995.8,"amount":71824.883},{"ts_code":"601226.SH","trade_date":"20260616","open":7.14,"high":7.32,"low":7.04,"close":7.19,"pre_close":7.11,"change":0.08,"pct_chg":1.1252,"vol":133428.0,"amount":95893.741},{"ts_code":"601226.SH","trade_date":"20260617","open":7.23,"high":7.25,"low":6.92,"close":6.98,"pre_close":7.19,"change":-0.21,"pct_chg":-2.9207,"vol":128761.0,"amount":90228.283},{"ts_code":"601226.SH","trade_date":"20260618","open":6.97,"high":6.98,"low":6.84,"close":6.88,"pre_close":6.98,"change":-0.1,"pct_chg":-1.4327,"vol":94785.99,"amount":65435.847},{"ts_code":"601226.SH","trade_date":"20260622","open":6.83,"high":6.92,"low":6.64,"close":6.9,"pre_close":6.88,"change":0.02,"pct_chg":0.2907,"vol":140780.43,"amount":95046.694},{"ts_code":"601226.SH","trade_date":"20260623","open":6.9,"high":7.04,"low":6.8,"close":6.81,"pre_close":6.9,"change":-0.09,"pct_chg":-1.3043,"vol":117739.0,"amount":81474.66},{"ts_code":"601226.SH","trade_date":"20260624","open":6.85,"high":6.86,"low":6.66,"close":6.74,"pre_close":6.81,"change":-0.07,"pct_chg":-1.0279,"vol":91992.13,"amount":61929.653},{"ts_code":"601226.SH","trade_date":"20260625","open":6.7,"high":6.83,"low":6.64,"close":6.68,"pre_close":6.74,"change":-0.06,"pct_chg":-0.8902,"vol":104093.72,"amount":69704.286},{"ts_code":"601226.SH","trade_date":"20260626","open":6.72,"high":7.35,"low":6.71,"close":7.05,"pre_close":6.68,"change":0.37,"pct_chg":5.5389,"vol":407618.72,"amount":293301.227},{"ts_code":"601226.SH","trade_date":"20260629","open":7.04,"high":7.06,"low":6.42,"close":6.55,"pre_close":7.0,"change":-0.45,"pct_chg":-6.4286,"vol":479764.59,"amount":317052.091},{"ts_code":"601226.SH","trade_date":"20260630","open":6.46,"high":6.65,"low":6.33,"close":6.36,"pre_close":6.55,"change":-0.19,"pct_chg":-2.9008,"vol":261905.87,"amount":167743.72},{"ts_code":"601226.SH","trade_date":"20260701","open":6.32,"high":6.5,"low":6.3,"close":6.43,"pre_close":6.36,"change":0.07,"pct_chg":1.1006,"vol":207763.8,"amount":133062.682},{"ts_code":"601226.SH","trade_date":"20260702","open":6.4,"high":6.58,"low":6.3,"close":6.31,"pre_close":6.43,"change":-0.12,"pct_chg":-1.8663,"vol":183862.5,"amount":118247.05},{"ts_code":"601226.SH","trade_date":"20260703","open":6.34,"high":6.62,"low":6.33,"close":6.56,"pre_close":6.31,"change":0.25,"pct_chg":3.962,"vol":203589.0,"amount":132557.242}]

# === Read CSV valuation data ===
# Resolve paths relative to project root (scripts/ -> parent)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(_PROJECT_ROOT, "data", "601226_consolidated.csv")
csv_data = {}
with open(csv_path, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_data[row["trade_date"]] = row

# === Merge: chronological order ===
tushare_data.sort(key=lambda x: x["trade_date"])

dates = []
ohlcv = []  # [open, close, low, high]
volumes = []
pe_list = []
pb_list = []
turnover_list = []
total_mv_list = []
amount_list = []
pct_chg_list = []

for item in tushare_data:
    td = item["trade_date"]
    # Format date as YYYY-MM-DD
    formatted_date = f"{td[:4]}-{td[4:6]}-{td[6:]}"
    dates.append(formatted_date)
    ohlcv.append([item["open"], item["close"], item["low"], item["high"]])
    volumes.append(round(item["vol"] / 10000, 2))  # convert to 万手
    amount_list.append(round(item["amount"] / 10000, 2))  # convert to 万元
    pct_chg_list.append(item["pct_chg"])

    csv_row = csv_data.get(td, {})
    pe_list.append(float(csv_row.get("pe", 0)) if csv_row.get("pe") else None)
    pb_list.append(float(csv_row.get("pb", 0)) if csv_row.get("pb") else None)
    turnover_list.append(float(csv_row.get("turnover_rate", 0)) if csv_row.get("turnover_rate") else None)
    total_mv_list.append(float(csv_row.get("total_mv", 0)) if csv_row.get("total_mv") else None)

# === Calculate MA lines ===
def calc_ma(data, period):
    result = []
    for i in range(len(data)):
        if i < period - 1:
            result.append(None)
        else:
            window = data[i-period+1:i+1]
            valid = [x for x in window if x is not None]
            result.append(round(sum(valid) / len(valid), 2) if valid else None)
    return result

closes = [d[1] for d in ohlcv]
ma5 = calc_ma(closes, 5)
ma10 = calc_ma(closes, 10)
ma20 = calc_ma(closes, 20)
ma60 = calc_ma(closes, 60)

# === Summary statistics ===
total_days = len(dates)
first_close = closes[0]
last_close = closes[-1]
total_return = round((last_close - first_close) / first_close * 100, 2)
highest = max(d[3] for d in ohlcv)
lowest = min(d[2] for d in ohlcv)
avg_vol = round(sum(volumes) / len(volumes), 2)

# Find highest/lowest dates
high_idx = max(range(len(ohlcv)), key=lambda i: ohlcv[i][3])
low_idx = min(range(len(ohlcv)), key=lambda i: ohlcv[i][2])

# Latest valuation metrics
latest_pe = pe_list[-1] if pe_list[-1] else None
latest_pb = pb_list[-1] if pb_list[-1] else None
latest_turnover = turnover_list[-1] if turnover_list[-1] else None
latest_mv = total_mv_list[-1] if total_mv_list[-1] else None

# === Generate HTML ===
html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>华电科工 (601226) 行情面板</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background: #f0f2f5;
    color: #333;
    padding: 20px;
}
.header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #fff;
    padding: 24px 32px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
.header-left h1 { font-size: 28px; margin-bottom: 6px; }
.header-left .subtitle { font-size: 14px; opacity: 0.7; }
.header-right { text-align: right; }
.header-right .price {
    font-size: 42px;
    font-weight: 700;
    font-family: 'Courier New', monospace;
}
.header-right .change {
    font-size: 18px;
    margin-top: 4px;
    font-family: 'Courier New', monospace;
}
.up-color { color: #e74c3c; }
.down-color { color: #2ecc71; }

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 14px;
    margin-bottom: 20px;
}
.stat-card {
    background: #fff;
    padding: 16px 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-2px); }
.stat-card .label {
    font-size: 12px;
    color: #999;
    margin-bottom: 6px;
}
.stat-card .value {
    font-size: 22px;
    font-weight: 600;
    font-family: 'Courier New', monospace;
}
.stat-card .unit { font-size: 13px; color: #aaa; font-weight: 400; }

.chart-container {
    background: #fff;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}
.chart-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 12px;
    color: #1a1a2e;
    border-left: 4px solid #e74c3c;
    padding-left: 10px;
}
.chart-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}
@media (max-width: 1200px) {
    .chart-row { grid-template-columns: 1fr; }
}
#kline-chart { width: 100%; height: 520px; }
#volume-chart { width: 100%; height: 220px; }
#pe-chart, #pb-chart, #turnover-chart, #mv-chart {
    width: 100%; height: 260px;
}
.footer {
    text-align: center;
    color: #999;
    font-size: 12px;
    padding: 16px;
}
.kline-wrapper {
    background: #fff;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}
</style>
</head>
<body>

<div class="header">
    <div class="header-left">
        <h1>华电科工 <span style="font-size:18px; opacity:0.6;">601226.SH</span></h1>
        <div class="subtitle">数据区间: __START_DATE__ ~ __END_DATE__ | 共 __TOTAL_DAYS__ 个交易日</div>
    </div>
    <div class="header-right">
        <div class="price" id="latest-price">__LATEST_PRICE__</div>
        <div class="change" id="latest-change">__LATEST_CHANGE__</div>
    </div>
</div>

<div class="stats-grid">
    <div class="stat-card">
        <div class="label">期间累计涨跌幅</div>
        <div class="value __RETURN_CLASS__">__TOTAL_RETURN__<span class="unit">%</span></div>
    </div>
    <div class="stat-card">
        <div class="label">最高价</div>
        <div class="value up-color">__HIGH__<span class="unit">元 (__HIGH_DATE__)</span></div>
    </div>
    <div class="stat-card">
        <div class="label">最低价</div>
        <div class="value down-color">__LOW__<span class="unit">元 (__LOW_DATE__)</span></div>
    </div>
    <div class="stat-card">
        <div class="label">日均成交量</div>
        <div class="value">__AVG_VOL__<span class="unit">万手</span></div>
    </div>
    <div class="stat-card">
        <div class="label">最新PE(TTM)</div>
        <div class="value">__LATEST_PE__</div>
    </div>
    <div class="stat-card">
        <div class="label">最新PB</div>
        <div class="value">__LATEST_PB__</div>
    </div>
    <div class="stat-card">
        <div class="label">最新换手率</div>
        <div class="value">__LATEST_TURNOVER__<span class="unit">%</span></div>
    </div>
    <div class="stat-card">
        <div class="label">最新总市值</div>
        <div class="value">__LATEST_MV__<span class="unit">万元</span></div>
    </div>
</div>

<div class="kline-wrapper">
    <div class="chart-title">K线图 & 成交量</div>
    <div id="kline-chart"></div>
    <div id="volume-chart"></div>
</div>

<div class="chart-row">
    <div class="chart-container">
        <div class="chart-title">市盈率 PE (TTM)</div>
        <div id="pe-chart"></div>
    </div>
    <div class="chart-container">
        <div class="chart-title">市净率 PB</div>
        <div id="pb-chart"></div>
    </div>
</div>

<div class="chart-row">
    <div class="chart-container">
        <div class="chart-title">换手率 (%)</div>
        <div id="turnover-chart"></div>
    </div>
    <div class="chart-container">
        <div class="chart-title">总市值 (亿元)</div>
        <div id="mv-chart"></div>
    </div>
</div>

<div class="footer">
    数据来源: Tushare (日线行情) + CSV汇总数据 (估值指标) | 生成时间: 2026-07-04 | 涨红跌绿（中国A股惯例）
</div>

<script>
// === Data ===
var dates = __DATES__;
var ohlcv = __OHLCV__;
var volumes = __VOLUMES__;
var ma5 = __MA5__;
var ma10 = __MA10__;
var ma20 = __MA20__;
var ma60 = __MA60__;
var peData = __PE__;
var pbData = __PB__;
var turnoverData = __TURNOVER__;
var mvData = __MV__;
var pctChgData = __PCT_CHG__;

// Chinese stock convention: red=up, green=down
var upColor = '#e74c3c';
var downColor = '#2ecc71';
var upBorderColor = '#c0392b';
var downBorderColor = '#27ae60';

// === K-line Chart ===
var klineChart = echarts.init(document.getElementById('kline-chart'));
var klineOption = {
    animation: false,
    tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross' },
        backgroundColor: 'rgba(255,255,255,0.95)',
        borderColor: '#ddd',
        textStyle: { color: '#333' },
        formatter: function(params) {
            var d = params[0];
            var idx = d.dataIndex;
            var o = ohlcv[idx][0], c = ohlcv[idx][1], l = ohlcv[idx][2], h = ohlcv[idx][3];
            var chg = pctChgData[idx];
            var color = c >= o ? upColor : downColor;
            var html = '<div style="font-size:13px;">';
            html += '<b>' + dates[idx] + '</b><br/>';
            html += '开盘: ' + o.toFixed(2) + '<br/>';
            html += '收盘: <span style="color:' + color + '">' + c.toFixed(2) + '</span><br/>';
            html += '最高: ' + h.toFixed(2) + '<br/>';
            html += '最低: ' + l.toFixed(2) + '<br/>';
            html += '涨跌幅: <span style="color:' + color + '">' + (chg >= 0 ? '+' : '') + chg.toFixed(2) + '%</span><br/>';
            html += '成交量: ' + volumes[idx].toFixed(1) + ' 万手';
            html += '</div>';
            return html;
        }
    },
    legend: {
        data: ['K线', 'MA5', 'MA10', 'MA20', 'MA60'],
        top: 5,
        textStyle: { fontSize: 12 }
    },
    grid: { left: '6%', right: '3%', top: 40, bottom: 50 },
    xAxis: {
        type: 'category',
        data: dates,
        boundaryGap: true,
        axisLine: { lineStyle: { color: '#999' } },
        axisLabel: { fontSize: 11, rotate: 0 },
        splitLine: { show: false }
    },
    yAxis: {
        type: 'value',
        scale: true,
        axisLine: { show: false },
        axisLabel: { fontSize: 11, formatter: function(v) { return v.toFixed(2); } },
        splitLine: { lineStyle: { color: '#f0f0f0' } }
    },
    dataZoom: [
        { type: 'inside', start: 0, end: 100 },
        { show: true, type: 'slider', bottom: 10, start: 0, end: 100, height: 20 }
    ],
    series: [
        {
            name: 'K线',
            type: 'candlestick',
            data: ohlcv,
            itemStyle: {
                color: upColor,
                color0: downColor,
                borderColor: upBorderColor,
                borderColor0: downBorderColor
            }
        },
        {
            name: 'MA5',
            type: 'line',
            data: ma5,
            smooth: true,
            symbol: 'none',
            lineStyle: { width: 1.5, color: '#f39c12' }
        },
        {
            name: 'MA10',
            type: 'line',
            data: ma10,
            smooth: true,
            symbol: 'none',
            lineStyle: { width: 1.5, color: '#3498db' }
        },
        {
            name: 'MA20',
            type: 'line',
            data: ma20,
            smooth: true,
            symbol: 'none',
            lineStyle: { width: 1.5, color: '#9b59b6' }
        },
        {
            name: 'MA60',
            type: 'line',
            data: ma60,
            smooth: true,
            symbol: 'none',
            lineStyle: { width: 1.5, color: '#1abc9c' }
        }
    ]
};
klineChart.setOption(klineOption);

// === Volume Chart ===
var volChart = echarts.init(document.getElementById('volume-chart'));
var volColors = ohlcv.map(function(d) {
    return d[1] >= d[0] ? upColor : downColor;
});
var volOption = {
    animation: false,
    tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        formatter: function(params) {
            var d = params[0];
            return '<b>' + dates[d.dataIndex] + '</b><br/>成交量: ' + d.value.toFixed(1) + ' 万手';
        }
    },
    grid: { left: '6%', right: '3%', top: 20, bottom: 30 },
    xAxis: {
        type: 'category',
        data: dates,
        boundaryGap: true,
        axisLine: { lineStyle: { color: '#999' } },
        axisLabel: { fontSize: 11 },
        splitLine: { show: false }
    },
    yAxis: {
        type: 'value',
        axisLine: { show: false },
        axisLabel: { fontSize: 11, formatter: function(v) { return v.toFixed(0); } },
        splitLine: { lineStyle: { color: '#f0f0f0' } }
    },
    dataZoom: [
        { type: 'inside', start: 0, end: 100 },
        { show: true, type: 'slider', bottom: 5, start: 0, end: 100, height: 16 }
    ],
    series: [{
        name: '成交量',
        type: 'bar',
        data: volumes.map(function(v, i) {
            return { value: v, itemStyle: { color: volColors[i] } };
        })
    }]
};
volChart.setOption(volOption);

// Sync zoom between kline and volume
klineChart.on('dataZoom', function(params) {
    var start = params.start !== undefined ? params.start : (params.batch ? params.batch[0].start : 0);
    var end = params.end !== undefined ? params.end : (params.batch ? params.batch[0].end : 100);
    volChart.dispatchAction({ type: 'dataZoom', start: start, end: end });
});
volChart.on('dataZoom', function(params) {
    var start = params.start !== undefined ? params.start : (params.batch ? params.batch[0].start : 0);
    var end = params.end !== undefined ? params.end : (params.batch ? params.batch[0].end : 100);
    klineChart.dispatchAction({ type: 'dataZoom', start: start, end: end });
});

// === PE Chart ===
var peChart = echarts.init(document.getElementById('pe-chart'));
peChart.setOption({
    tooltip: { trigger: 'axis', formatter: function(p) { return '<b>' + p[0].name + '</b><br/>PE(TTM): ' + (p[0].value ? p[0].value.toFixed(2) : 'N/A'); } },
    grid: { left: '8%', right: '5%', top: 20, bottom: 30 },
    xAxis: { type: 'category', data: dates, axisLabel: { fontSize: 10, rotate: 30 } },
    yAxis: { type: 'value', scale: true, axisLabel: { fontSize: 10 } },
    dataZoom: [{ type: 'inside', start: 0, end: 100 }],
    series: [{ name: 'PE', type: 'line', data: peData, symbol: 'none', areaStyle: { color: 'rgba(52,152,219,0.1)' }, lineStyle: { color: '#3498db', width: 1.5 } }]
});

// === PB Chart ===
var pbChart = echarts.init(document.getElementById('pb-chart'));
pbChart.setOption({
    tooltip: { trigger: 'axis', formatter: function(p) { return '<b>' + p[0].name + '</b><br/>PB: ' + (p[0].value ? p[0].value.toFixed(2) : 'N/A'); } },
    grid: { left: '8%', right: '5%', top: 20, bottom: 30 },
    xAxis: { type: 'category', data: dates, axisLabel: { fontSize: 10, rotate: 30 } },
    yAxis: { type: 'value', scale: true, axisLabel: { fontSize: 10 } },
    dataZoom: [{ type: 'inside', start: 0, end: 100 }],
    series: [{ name: 'PB', type: 'line', data: pbData, symbol: 'none', areaStyle: { color: 'rgba(155,89,182,0.1)' }, lineStyle: { color: '#9b59b6', width: 1.5 } }]
});

// === Turnover Chart ===
var turnoverChart = echarts.init(document.getElementById('turnover-chart'));
turnoverChart.setOption({
    tooltip: { trigger: 'axis', formatter: function(p) { return '<b>' + p[0].name + '</b><br/>换手率: ' + (p[0].value ? p[0].value.toFixed(2) + '%' : 'N/A'); } },
    grid: { left: '8%', right: '5%', top: 20, bottom: 30 },
    xAxis: { type: 'category', data: dates, axisLabel: { fontSize: 10, rotate: 30 } },
    yAxis: { type: 'value', axisLabel: { fontSize: 10, formatter: '{value}%' } },
    dataZoom: [{ type: 'inside', start: 0, end: 100 }],
    series: [{ name: '换手率', type: 'bar', data: turnoverData, itemStyle: { color: '#e67e22' } }]
});

// === Market Value Chart ===
var mvChart = echarts.init(document.getElementById('mv-chart'));
var mvYi = mvData.map(function(v) { return v ? Math.round(v / 10000 * 100) / 100 : null; }); // 万元 -> 亿元
mvChart.setOption({
    tooltip: { trigger: 'axis', formatter: function(p) { return '<b>' + p[0].name + '</b><br/>总市值: ' + (p[0].value ? p[0].value.toFixed(2) + ' 亿元' : 'N/A'); } },
    grid: { left: '8%', right: '5%', top: 20, bottom: 30 },
    xAxis: { type: 'category', data: dates, axisLabel: { fontSize: 10, rotate: 30 } },
    yAxis: { type: 'value', scale: true, axisLabel: { fontSize: 10, formatter: '{value}亿' } },
    dataZoom: [{ type: 'inside', start: 0, end: 100 }],
    series: [{ name: '总市值', type: 'line', data: mvYi, symbol: 'none', areaStyle: { color: 'rgba(231,76,60,0.1)' }, lineStyle: { color: '#e74c3c', width: 1.5 } }]
});

// Resize handler
window.addEventListener('resize', function() {
    klineChart.resize();
    volChart.resize();
    peChart.resize();
    pbChart.resize();
    turnoverChart.resize();
    mvChart.resize();
});
</script>
</body>
</html>"""

# Fill in template
last_pct = pct_chg_list[-1]
return_class = "up-color" if total_return >= 0 else "down-color"
latest_change_color = "up-color" if last_pct >= 0 else "down-color"
latest_change_str = f"{'+' if last_pct >= 0 else ''}{last_pct:.2f}%  {'+' if closes[-1] - tushare_data[-1]['pre_close'] >= 0 else ''}{(closes[-1] - tushare_data[-1]['pre_close']):.2f}"

html = html_template \
    .replace("__START_DATE__", dates[0]) \
    .replace("__END_DATE__", dates[-1]) \
    .replace("__TOTAL_DAYS__", str(total_days)) \
    .replace("__LATEST_PRICE__", f"{last_close:.2f}") \
    .replace("__LATEST_CHANGE__", latest_change_str) \
    .replace("__TOTAL_RETURN__", f"{'+' if total_return >= 0 else ''}{total_return}") \
    .replace("__RETURN_CLASS__", return_class) \
    .replace("__HIGH__", f"{highest:.2f}") \
    .replace("__HIGH_DATE__", dates[high_idx]) \
    .replace("__LOW__", f"{lowest:.2f}") \
    .replace("__LOW_DATE__", dates[low_idx]) \
    .replace("__AVG_VOL__", f"{avg_vol:.1f}") \
    .replace("__LATEST_PE__", f"{latest_pe:.1f}" if latest_pe else "N/A") \
    .replace("__LATEST_PB__", f"{latest_pb:.2f}" if latest_pb else "N/A") \
    .replace("__LATEST_TURNOVER__", f"{latest_turnover:.2f}" if latest_turnover else "N/A") \
    .replace("__LATEST_MV__", f"{latest_mv/10000:.1f}" if latest_mv else "N/A") \
    .replace("__DATES__", json.dumps(dates)) \
    .replace("__OHLCV__", json.dumps(ohlcv)) \
    .replace("__VOLUMES__", json.dumps(volumes)) \
    .replace("__MA5__", json.dumps(ma5)) \
    .replace("__MA10__", json.dumps(ma10)) \
    .replace("__MA20__", json.dumps(ma20)) \
    .replace("__MA60__", json.dumps(ma60)) \
    .replace("__PE__", json.dumps(pe_list)) \
    .replace("__PB__", json.dumps(pb_list)) \
    .replace("__TURNOVER__", json.dumps(turnover_list)) \
    .replace("__MV__", json.dumps(total_mv_list)) \
    .replace("__PCT_CHG__", json.dumps(pct_chg_list))

# Fix the change color in header
html = html.replace(
    '<div class="change" id="latest-change">',
    f'<div class="change {latest_change_color}" id="latest-change">'
)

output_path = os.path.join(_PROJECT_ROOT, "output", "601226_dashboard.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Dashboard generated: {output_path}")
print(f"Data range: {dates[0]} ~ {dates[-1]}")
print(f"Total trading days: {total_days}")
print(f"Period return: {'+' if total_return >= 0 else ''}{total_return}%")
print(f"Highest: {highest:.2f} on {dates[high_idx]}")
print(f"Lowest: {lowest:.2f} on {dates[low_idx]}")
print(f"Latest close: {last_close:.2f}")

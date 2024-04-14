@echo off
cd C:\Pessoal\github\QA_API_Test_Collection - Copia
echo QA_API_Test_Collection
echo Testes das API da Squad PDV em ambiente Produtivo
echo Executando teste...
robot -d ./logs -x output-xml tests
echo Teste concluido.
@echo echo Preparando resultado dos testes...
@echo python ReportTeams.py
del /q /s "C:\Pessoal\github\Telegram_Bot_QA\Resultados"
xcopy "C:\Pessoal\github\QA_API_Test_Collection - Copia\logs" "C:\Pessoal\github\Telegram_Bot_QA\Resultados" /s /e
@echo fim
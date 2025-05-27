MN Counter
por Rodrigo Noronha de Mello
https://github.com/vonroderik

📌 Sobre o Projeto
MN Counter é um programa em Python que facilita a contagem de células nucleadas (núcleos) e danos celulares em lâminas de análise. Utilizando atalhos de teclado, o usuário registra eventos rapidamente, com todos os dados salvos automaticamente em arquivos CSV dentro de uma pasta `data/`. Além disso, é possível consultar a contagem parcial a qualquer momento durante o processo.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Como Executar o Programa

Para rodar o MN Counter, basta clicar no arquivo executável MN_Counter.exe.
Caso queira iniciar via terminal, siga os passos:

cd caminho/para/o/programa
MN_Counter.exe

Após a execução, o programa exibirá um menu com as seguintes opções:  
📌 1 - Contagem de Núcleos  
📌 2 - Contagem de Danos  
📌 3 - Resumo da Contagem  
📌 4 - Sair  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔬 Contagem de Núcleos

Selecione a opção 1 - Contagem de Núcleos e informe o ID da lâmina que deseja analisar.  
Use os seguintes atalhos de teclado para marcar as células corretamente:  

──────────────────────  
 Tecla       Função               
──────────────────────  
 1           M1 (Mononuclear)   
 2           M2 (Binuclear)     
 3           M3 (Trinuclear)    
 4           M4 (Tetranuclear)  
 5           NEC (Necrose)      
 6           AP (Apoptose)      
 7           IDNC (Indefinido)  
TAB         Mostrar contagem parcial
ESC         Abortar manualmente
──────────────────────

Limite total: o programa emite um **beep** e retorna ao menu automaticamente quando a soma de células com núcleo (M1, M2, M3, M4, IDNC) atingir **500 eventos**. NEC e AP não são considerados nesse limite.

Para consultar a contagem parcial durante o processo, pressione **TAB**. Para abortar antes do limite, pressione **ESC**.  
O resumo é salvo em `data/nucleos.csv`.  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧬 Contagem de Danos  

Escolha a opção 2 - Contagem de Danos e insira o ID da lâmina.  
Use os seguintes atalhos para marcar os danos celulares:  

──────────────────────────────  
 Tecla       Função                        
──────────────────────────────  
 Q           BN (Binucleadas)              
 W           MN (Micronúcleo)              
 E           NBUD (Nuclear Budding)        
 R           NPB (Nucleoplasmic Bridge)    
TAB         Mostrar contagem parcial
ESC         Abortar manualmente
──────────────────────────────  

Limite específico: ao atingir **1000 BN**, o programa emite um **beep** e retorna ao menu automaticamente.  
Para consultar a contagem parcial durante o processo, pressione **TAB**. Para abortar antes do limite, pressione **ESC**.  
O resumo é salvo em `data/danos.csv`.  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Exibir Resumo Geral  

Escolha a opção 3 - Resumo da Contagem para ver os dados registrados.  
O programa acessará os arquivos CSV e os exibirá formatados, permitindo a revisão das contagens sem precisar abrir os arquivos manualmente.  
Caso queira abrir os arquivos CSV, eles estarão na mesma pasta do executável (dentro da pasta `data/`).  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

❓ Possíveis Problemas e Soluções  

✅ Erro ao salvar CSV? → Verifique se o programa tem permissão para gravar na pasta.  
✅ Executável não abre? → Teste rodar pelo terminal (cmd) e veja se há mensagens de erro.  
✅ Teclas de atalho não funcionam? → Certifique-se de que o programa está rodando em um terminal compatível e com foco na janela.  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

🛠 Tecnologias Utilizadas  
✔ Python  
✔ keyboard → Captura de teclas de atalho  
✔ tabulate → Exibição formatada dos dados  
✔ csv → Manipulação de arquivos  
✔ PyInstaller → Conversão para executável  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

*Última atualização: maio de 2025*

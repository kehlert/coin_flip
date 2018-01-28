import numpy as np
from beautifultable import BeautifulTable

p = 0.55
initial_wealth = 100

user_data = {}
wealth = {}

coin_str = '''
        _.-'~~`~~'-._
     .'`  B   E   R  `'.
    / I               T \\
  /`       .-'~"-.       `\\
 ; L      / `-    \      Y ;
;        />  `.  -.|        ;
|       /_     '-.__)       |
|        |-  _.' \ |        |
;        `~~;     \\        ;
 ;IN MATH WE/      \\)P    ;
  \  TRUST '.___.-'`"     /
   `\                   /`
     '._   2 0 1 8   _.'
        `'-..,,,..-'`'''

def update_table(table, wealth):
    table_names = list(table['Name'])
    for (index, name) in enumerate(table_names):
        table[index]['Wealth'] = wealth[name]
    table.sort('Wealth', reverse=True)

def get_first_second_ratio(wealth):
    #get 'distance' between 1st and 2nd place
    sorted_wealth = list(sorted(wealth.values(), reverse=True))
    if not sorted_wealth[1] == 0:
        ratio = float(sorted_wealth[0]) / sorted_wealth[1]
    else:
        ratio = float('inf')
    return ratio

########
## get names and bets
########
print(coin_str)
print('You WIN if the coin comes up heads.')
print('Probability of heads = {:.2f}'.format(p))
print('Your initial wealth: ${:.0f}\n'.format(initial_wealth))
print('You can bet a FIXED amount (e.g. $1) on every turn,\n\
or a PERCENTAGE (e.g. 50%) of your current wealth on every turn.\n')

while True:
    name = input('Enter name: ')
    if name == '':
        break
    else:
        bet = input('Enter bet: ')
    bet_percent = (bet[-1] == '%')
    numeric_bet = float(bet.rstrip('%'))
    if bet_percent:
        numeric_bet = float(numeric_bet) / 100
    user_data[name] = (numeric_bet, bet_percent)
    print('')

#user_data = {'kurt': (2, False), 'anna': (0.2, True), 'steve': (0.3, True)} 
wealth = dict.fromkeys(user_data.keys(), initial_wealth)

########
## create the output table
########
table = BeautifulTable()
table.column_headers = ['Name', 'Bet', 'Wealth']
for (name, bet) in user_data.items():
    bet_str = None
    #if betting a percentage
    if bet[1]:
        bet_str = '{:.0%}'.format(bet[0])
    else:
        bet_str = str(bet[0])
    table.append_row([name, bet_str, wealth[name]])

#######
##run the simulation
#######
while True:
    print(table)
    print('Ratio between 1st and 2nd place wealth: {0:.1f}\n'.format(get_first_second_ratio(wealth)))

    #flip coins
    flips = input('# of coins to flip ("r" to reset): ')
    print('')
    if flips == '0':
        break 
    elif flips == 'r':
        wealth = dict.fromkeys(user_data.keys(), initial_wealth)
        update_table(table, wealth)
        continue
    
    flip_results = 2 * np.random.binomial(1, p, int(flips)) - 1
    
    #update wealth
    for (name, bet) in user_data.items():
        numeric_bet = bet[0]
        #if betting a percentage
        if bet[1] == True:
            wealth[name] *= np.prod(1 + numeric_bet * flip_results)
        else:
            #check for bankruptcy
            if wealth[name] > 0:
                running_wealth = wealth[name] + np.cumsum(numeric_bet * flip_results)
                if any(running_wealth < 0):
                    wealth[name] = 0
                else:
                    wealth[name] += np.sum(numeric_bet * flip_results)
    
    update_table(table, wealth)


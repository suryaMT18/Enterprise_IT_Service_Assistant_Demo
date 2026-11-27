from app.tools import get_asset,get_ticket,list_support_teams

# print("Valid Asset")
# print(get_asset("AST-1002"))

# print("\nUNKNOWN ASSET")
# print(get_asset("AST-9999"))

# print("\nLOWERCASE INPUT")
# print(get_asset("ast-1002"))

# print("\nEMPTY INPUT")
# print(get_asset(""))



# print("VALID TICKET")
# print(get_ticket("INC-2041"))

# print("\nUNKNOWN TICKET")
# print(get_ticket("INC-9999"))

# print("\nLOWERCASE INPUT")
# print(get_ticket("inc-2041"))

# print("\nEMPTY INPUT")
# print(get_ticket(""))


result = list_support_teams()

print("AVAILABLE SUPPORT TEAMS")

for team in result["teams"]:
    print("\nTeam:", team["team_name"])
    print("Responsibility:", team["responsibility"])
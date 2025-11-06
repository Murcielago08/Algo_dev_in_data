def rps(a: str, b: str) -> str:
    """Pierre-papier-ciseaux"""
    a = a.lower()
    b = b.lower()
    valid = {'rock', 'paper', 'scissors'}
    if a not in valid or b not in valid:
        raise ValueError('Invalid choice')
    if a == b:
        return 'draw'
    wins = {('rock','scissors'), ('scissors','paper'), ('paper','rock')}
    return 'player1' if (a,b) in wins else 'player2'

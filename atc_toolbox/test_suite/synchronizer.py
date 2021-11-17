from atc_toolbox.test_suite.manager import load_ledger, get_excess, remove_excess, get_missing, download_missing, verify_data

if __name__ == '__main__':
    ledger = load_ledger()

    excess = get_excess(ledger)

    if excess:
        print(f'Your data folder contains {len(excess)} files not in the ledger. Would you like to delete them?')
        answer = input('(y/n) ')
        if answer.lower() == 'y':
            remove_excess(excess)
    else:
        print('No excess files.')

    missing = get_missing(ledger)
    if missing:
        print(f'You are missing {len(missing)} data tables, would you like to download them now?')
        answer = input('(y/n) ')
        if answer.lower() == 'y':
            download_missing(missing)
    else:
        print('No missing files.')

    print('Verifying data...')
    removed = verify_data()
    if removed:
        print(f'{len(removed)} files were empty and have been removed.')
    else:
        print('All files valid.')

    print('All files up to date.')
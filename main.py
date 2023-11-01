from website import create_app

app = create_app()

if __name__ == '__main__': #this means only if we run this file not if we import it. We do this so if you improt this main fiel somewhere else it doesnt just automaticly run the server
    app.run(debug=True)  #debug true means the web server is refreshed auto every time we make a change
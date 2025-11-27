import React from 'react';
import { ApolloProvider } from '@apollo/client';
import { client } from './apollo/client';
import { UserList } from './components/UserList';
import './App.css';

function App() {
    return (
        <ApolloProvider client={client}>
            <div className="App">
                <header className="App-header">
                    <h1>GraphQL FastAPI Demo</h1>
                </header>
                <main>
                    <UserList />
                </main>
            </div>
        </ApolloProvider>
    );
}

export default App;

import * as React from 'react';

import { BrowserRouter as Router, Redirect } from 'react-router-dom';
import Auth, { useAuthUser, useAuthActions } from 'use-eazy-auth';
import { AuthRoute, GuestRoute, MaybeAuthRoute } from 'use-eazy-auth/routes';

import Base from './containers/Base';
import SignIn from './containers/SignIn';


type LoginRequestPayload = {
  username: string,
  password: string,
};

const loginCall = (payload: LoginRequestPayload) => {
  const { username, password } = payload;
  return fetch('/api/auth/token/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
    headers: {
      'Content-Type': 'application/json'
    },
  }).then(response => {
    if (response.ok) {
      return response.json()
    } else {
      throw new Error("Invalid credentials");
    }
  }).then(data => ({
    accessToken: data.access,
    refreshToken: data.refresh,
  }));
}

const meCall = (accessToken: string) => fetch('/api/auth/me/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  },
}).then(response => response.json());


const refreshTokenCall = (refreshToken: string) => fetch('/api/auth/token/refresh/', {
  method: 'POST',
  body: JSON.stringify({ token: refreshToken }),
  headers: {
    'Content-Type': 'application/json'
  },
}).then(response => response.json()).then(data => ({
  // NOTE: WE MUST ENFORCE THIS SHAPE! In order to make use-eazy-auth
  // understand your data!
  accessToken: data.access,
  refreshToken: data.refresh,
}))

function HomePage() {
  const { user } = useAuthUser();
  const { logout } = useAuthActions();
  if (user?.is_active) {
    return <Redirect to='/site' />;
  }
  logout();
  return <Redirect to='/login' />
}


export default function App() {

  return (
    <Auth
      loginCall={loginCall}
      meCall={meCall}
      refreshTokenCall={refreshTokenCall}
    >
      <Router>
        <AuthRoute
          // Guest user go to /login
          redirectTo='/login'
          path='/report'
        >
          <div>Report page</div>
        </AuthRoute>

        <AuthRoute
          redirectTo='/login'
          path='/site'
        >
          <Base />
        </AuthRoute>

        <MaybeAuthRoute path='/' exact>
          <HomePage />
        </MaybeAuthRoute>

        <GuestRoute path='/login'>
          <SignIn />
        </GuestRoute>

      </Router>

    </Auth>
  );
}

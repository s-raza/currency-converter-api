import CurrencyApp from './components/currencyApp';
import { RequireLogin } from './components/pages/login';

function App() {

  return (
    <RequireLogin>
      <CurrencyApp />
    </RequireLogin>
  );
}

export default App;

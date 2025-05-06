import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

interface ReactQueryProviderProps {
  children: React.ReactNode;
}

const queryClient = new QueryClient();

function ReactQueryProvider({ children }: ReactQueryProviderProps) {
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

export { ReactQueryProvider };

export type { ReactQueryProviderProps };

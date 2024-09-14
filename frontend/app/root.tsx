import {
    json,
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
  useLoaderData,
} from "@remix-run/react";
import type { LinksFunction } from "@remix-run/node";

import "./tailwind.css";
import { QueryClient, QueryClientProvider } from "react-query";

export const links: LinksFunction = () => [
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  {
    rel: "preconnect",
    href: "https://fonts.gstatic.com",
    crossOrigin: "anonymous",
  },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
  },
];

const queryClient = new QueryClient()

export function loader() {
  return json({
    ENV: {
      SUNO_API_KEY: process.env.SUNO_API_KEY
    }
  })
}
 
export function Layout({ children }: { children: React.ReactNode }) {  
  const data = useLoaderData<typeof loader>();
  return (
    
      <html lang="en">
        <head>
          <meta charSet="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <Meta />
          <Links />
        </head>
        <body>
          <script
              dangerouslySetInnerHTML={{
                __html: `window.ENV = ${JSON.stringify(
                  data.ENV
                )}`,
              }}
            />
            {children}
            <ScrollRestoration />
            <Scripts />
        </body>
      </html>
    
  );
}

export default function App() {
  
  return (
    <QueryClientProvider client={queryClient}>
      <Outlet />
      
    </QueryClientProvider>
  );
}

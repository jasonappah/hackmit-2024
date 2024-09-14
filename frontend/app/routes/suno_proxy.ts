import type { LoaderFunctionArgs } from "@remix-run/node"; // or cloudflare/deno
import { json } from "@remix-run/node"; // or cloudflare/deno
import { SUNO_BASE_URL } from "~/lib/constants";

export async function loader({
  request,
}: LoaderFunctionArgs) {
  const url = new URL(request.url)
  const e = url.searchParams.get("endpoint")
  if (!e) {
    throw new Error("missing endpoint")
  }
  
  
  
  const body = request.method.toLowerCase() !== 'get' ? await request.json() : undefined
  console.log(body)
  const res = await fetch(SUNO_BASE_URL + e, {
    headers: {
      
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.SUNO_API_KEY}`,
      
    },
      method: request.method,
      body: body  ? JSON.stringify(body) : undefined
  })

    const data = await res.json();
    
    return json(data)
  
}

export const action = loader
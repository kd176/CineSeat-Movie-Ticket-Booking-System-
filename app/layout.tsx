import type { Metadata } from 'next';
export const metadata: Metadata = {title:'CineSeat — Book your next movie night',description:'Discover 56 movies, worldwide Simkl trends and smart group seating. Book and manage your cinema demo tickets across devices.'};
export default function RootLayout({children}:{children:React.ReactNode}) {return <html lang="en"><head><link rel="stylesheet" href="/web/style.css"/><link rel="stylesheet" href="/web/final.css"/></head><body>{children}</body></html>}

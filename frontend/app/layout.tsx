import type {Metadata} from 'next';
import './globals.css';
export const metadata:Metadata={title:'Relay Discipline — Handoff Network',description:'Semantic handoff validation powered by GenLayer'};
export default function Layout({children}:{children:React.ReactNode}){return <html lang="en" suppressHydrationWarning><body suppressHydrationWarning>{children}</body></html>}

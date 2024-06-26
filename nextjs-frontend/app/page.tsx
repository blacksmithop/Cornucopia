import styles from '@/app/ui/home.module.css';
import { ArrowRightIcon } from '@heroicons/react/24/outline';
import NavBar from "@/app/ui/navbar"
import Footer from "@/app/ui/footer"
import Content from "@/app/ui/content"

export default function Page() {
  return (
    <main >
        <div className="flex flex-col h-screen justify-between">
        <NavBar />
        <Content />
        <Footer />
      </div>
    </main>
  );
}

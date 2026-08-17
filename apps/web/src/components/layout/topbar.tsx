"use client";

import { useAuthStore } from "@/stores/auth-store";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { LogOut, Bell } from "lucide-react";

export function Topbar() {
  const { user, logout } = useAuthStore();

  return (
    <header className="flex h-16 shrink-0 items-center gap-4 border-b bg-background px-6">
      <div className="flex-1" />
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" className="text-muted-foreground">
          <Bell className="size-5" />
        </Button>
        <div className="flex items-center gap-3">
          <div className="flex flex-col items-end">
            <span className="text-sm font-medium leading-none">{user?.name || "Researcher"}</span>
            <span className="text-xs text-muted-foreground mt-1">{user?.email || "user@example.com"}</span>
          </div>
          <Avatar className="size-8 border">
            <AvatarFallback className="bg-primary/20 text-primary-foreground text-xs font-semibold">
              {user?.name?.charAt(0) || "R"}
            </AvatarFallback>
          </Avatar>
        </div>
        <Button variant="ghost" size="icon" onClick={logout} title="Log out" className="text-muted-foreground hover:text-destructive">
          <LogOut className="size-5" />
        </Button>
      </div>
    </header>
  );
}

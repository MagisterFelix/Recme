declare global {
  namespace model {
    interface User {
      id: number;
      name: string;
      email: string;
      image: string;
    }
    interface Filter {
      id: number;
      name: string;
      options: string[];
      icon: string;
    }
    interface Category {
      id: number;
      name: string;
      icon: string;
    }
    interface Location {
      id: number;
      image: string;
      rating: {
        avg: number | null;
        user: number | null;
      };
      name: string;
      latitude: number;
      longitude: number;
      category: Category;
    }
    interface Condition {
      context: string;
      choice: string;
    }
    interface Preference {
      filter: string;
      choice: string;
    }
    interface Recommendation {
      id: number;
      filters: {
        conditions: Condition[];
        preferences: Preference[];
      };
      is_liked: boolean | null;
      created_at: string;
      user: User;
      location: Location;
    }
    interface History {
      filters: {
        conditions: Condition[];
        preferences: Preference[];
      };
      recommendations: Recommendation[];
    }
    interface Review {
      id: number;
      rating: number;
      created_at: string;
      user: User;
      location: Location;
    }
  }
  namespace request {
    interface Authorization {
      email: string;
      password: string;
    }
    interface Registration {
      name: string;
      email: string;
      password: string;
    }
    interface UserUpdating {
      name: string;
      email: string;
      image: string;
    }
    interface PasswordChanging {
      password: string;
      new_password: string;
    }
    interface Reviewing {
      location: number;
      rating: number;
    }
    interface Estimating {
      is_liked: boolean | null;
    }
  }
  namespace response {
    interface Authorization {
      access: string;
      user: model.User;
    }
    interface Registration {
      name: string;
      email: string;
    }
  }
}

export {};
